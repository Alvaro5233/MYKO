"""
Pedidos MYKO: recibe los datos de envío, los valida con esquema_envio.json,
simula el pago y guarda el pedido en SQLite (myko.db).

Integración con carrito.py (dos líneas, después de crear `app`):

    from pedidos import registrar_pedidos
    registrar_pedidos(app, obtener_carrito)

`obtener_carrito(id_carrito)` la escribe carrito.py y debe regresar una lista de
renglones con: numero_de_producto, nombre_producto, cantidad, monto_total.
El total del pedido se calcula con esos renglones (precios del catálogo de
carrito.py), nunca con lo que mande el navegador.

Para probar sin carrito.py:  python pedidos.py   (puerto 5000)
Dependencias:                pip install flask jsonschema
"""

import json
import os
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone

from flask import Blueprint, Flask, jsonify, request
from jsonschema import Draft202012Validator, FormatChecker

CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_ESQUEMA = os.path.join(CARPETA, "esquema_envio.json")
RUTA_DB = os.path.join(CARPETA, "myko.db")

with open(RUTA_ESQUEMA, encoding="utf-8") as f:
    ESQUEMA = json.load(f)
VALIDADOR = Draft202012Validator(ESQUEMA, format_checker=FormatChecker())

CAMPOS_ENVIO = list(ESQUEMA["properties"]["envio"]["properties"].keys())
CAMPOS_OPCIONALES = ("numero_interior", "referencias")

# Mensajes en español por campo, para cuando no aplica uno genérico.
MENSAJES_CAMPO = {
    "nombre_completo": "Escribe tu nombre completo (solo letras).",
    "telefono": "El teléfono debe tener 10 dígitos.",
    "correo": "Escribe un correo válido.",
    "calle": "Escribe la calle.",
    "numero_exterior": "Escribe el número exterior.",
    "colonia": "Escribe la colonia.",
    "codigo_postal": "El código postal debe tener 5 dígitos.",
    "ciudad": "Escribe una ciudad válida (solo letras).",
    "estado": "Elige un estado de la lista.",
    "acepta_aviso_privacidad": "Debes aceptar el aviso de privacidad.",
    "id_carrito": "Carrito no válido.",
    "codigo_de_cliente": "Cliente no válido.",
}


# ---------- Validación ----------

def normalizar(datos):
    """Quita espacios sobrantes, limpia el teléfono y descarta opcionales vacíos."""
    envio = datos.get("envio")
    if not isinstance(envio, dict):
        return datos
    limpio = {}
    for campo, valor in envio.items():
        if isinstance(valor, str):
            valor = valor.strip()
            if campo == "telefono":
                valor = re.sub(r"[\s\-().]", "", valor)
            if campo in CAMPOS_OPCIONALES and valor == "":
                continue
        limpio[campo] = valor
    return dict(datos, envio=limpio)


def traducir_errores(datos):
    """Corre el esquema y regresa {campo: mensaje} con el primer error de cada campo."""
    errores = {}
    for error in VALIDADOR.iter_errors(datos):
        if error.validator == "required":
            for campo in error.validator_value:
                if campo not in error.instance:
                    errores.setdefault(campo, "Este campo es obligatorio.")
            continue
        if error.validator == "additionalProperties":
            errores.setdefault("_general", "La solicitud trae campos no permitidos.")
            continue
        rutas = [p for p in error.path if isinstance(p, str)]
        campo = rutas[-1] if rutas else "_general"
        if error.validator == "maxLength":
            mensaje = "Máximo {} caracteres.".format(error.validator_value)
        else:
            mensaje = MENSAJES_CAMPO.get(campo, "Dato no válido.")
        errores.setdefault(campo, mensaje)
    return errores


# ---------- Pago simulado ----------

def simular_pago(total):
    # Aquí irá la llamada al proveedor de pagos real. MYKO nunca recibe ni guarda
    # datos de tarjeta: el proveedor los captura y nos regresa solo una referencia.
    return {"estado": "aprobado", "referencia": "SIM-" + uuid.uuid4().hex[:10].upper()}


# ---------- Base de datos ----------

def conectar():
    con = sqlite3.connect(RUTA_DB)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def crear_tablas():
    with closing(conectar()) as con, con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_carrito INTEGER NOT NULL UNIQUE,
                codigo_de_cliente INTEGER NOT NULL,
                nombre_completo TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                calle TEXT NOT NULL,
                numero_exterior TEXT NOT NULL,
                numero_interior TEXT,
                colonia TEXT NOT NULL,
                codigo_postal TEXT NOT NULL,
                ciudad TEXT NOT NULL,
                estado TEXT NOT NULL,
                referencias TEXT,
                total REAL NOT NULL,
                estado_pago TEXT NOT NULL,
                referencia_pago TEXT NOT NULL,
                acepto_aviso_en TEXT NOT NULL,
                creado_en TEXT NOT NULL
            )""")
        con.execute("""
            CREATE TABLE IF NOT EXISTS pedido_productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
                numero_de_producto INTEGER,
                nombre_producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                monto_total REAL NOT NULL
            )""")


def guardar_pedido(datos, renglones, total, pago):
    envio = datos["envio"]
    ahora = datetime.now(timezone.utc).isoformat()
    columnas = ["id_carrito", "codigo_de_cliente"] + CAMPOS_ENVIO + [
        "total", "estado_pago", "referencia_pago", "acepto_aviso_en", "creado_en"]
    valores = [datos["id_carrito"], datos["codigo_de_cliente"]] + [
        envio.get(c) for c in CAMPOS_ENVIO] + [
        total, pago["estado"], pago["referencia"], ahora, ahora]

    with closing(conectar()) as con, con:
        cur = con.execute(
            "INSERT INTO pedidos ({}) VALUES ({})".format(
                ", ".join(columnas), ", ".join("?" * len(columnas))),
            valores)
        pedido_id = cur.lastrowid
        con.executemany(
            "INSERT INTO pedido_productos (pedido_id, numero_de_producto, nombre_producto,"
            " cantidad, monto_total) VALUES (?, ?, ?, ?, ?)",
            [(pedido_id, r.get("numero_de_producto"), r["nombre_producto"],
              int(r["cantidad"]), float(r["monto_total"])) for r in renglones])
    return pedido_id


# ---------- Endpoint ----------

def registrar_pedidos(app, obtener_carrito, vaciar_carrito=None):
    """Agrega POST /pedidos a la app de Flask. `vaciar_carrito(id_carrito)` es opcional."""
    crear_tablas()
    bp = Blueprint("pedidos", __name__)

    @bp.route("/pedidos", methods=["POST"])
    def crear_pedido():
        datos = request.get_json(silent=True)
        if not isinstance(datos, dict):
            return jsonify(error="La solicitud debe ser un JSON válido."), 400

        datos = normalizar(datos)
        errores = traducir_errores(datos)
        if errores:
            return jsonify(error="Revisa los datos de envío.", errores=errores), 422

        renglones = obtener_carrito(datos["id_carrito"]) or []
        if not renglones:
            return jsonify(error="Tu carrito está vacío."), 400

        total = round(sum(float(r["monto_total"]) for r in renglones), 2)
        pago = simular_pago(total)
        if pago["estado"] != "aprobado":
            return jsonify(error="El pago no fue aprobado."), 402

        try:
            numero_pedido = guardar_pedido(datos, renglones, total, pago)
        except sqlite3.IntegrityError:
            return jsonify(error="Este carrito ya tiene un pedido."), 409

        if vaciar_carrito:
            vaciar_carrito(datos["id_carrito"])

        return jsonify(
            numero_pedido=numero_pedido,
            total=total,
            estado_pago=pago["estado"],
            referencia_pago=pago["referencia"],
        ), 201

    app.register_blueprint(bp)


# ---------- Modo de prueba sin carrito.py ----------

if __name__ == "__main__":
    app = Flask(__name__)

    CATALOGO = {
        101: ("Cápsulas Melena de León", 300),
        102: ("Polvo Melena de León", 300),
    }
    CARRITOS = {}  # id_carrito -> lista de renglones, solo en memoria

    @app.after_request
    def permitir_cors(respuesta):
        respuesta.headers["Access-Control-Allow-Origin"] = "*"
        respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
        respuesta.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return respuesta

    @app.route("/carrito/agregar", methods=["POST"])
    def agregar():
        datos = request.get_json(silent=True) or {}
        producto = CATALOGO.get(datos.get("numero_de_producto"))
        cantidad = datos.get("cantidad")
        if not producto:
            return jsonify(error="Producto no encontrado."), 404
        if not isinstance(cantidad, int) or not 1 <= cantidad <= 10:
            return jsonify(error="La cantidad debe ser de 1 a 10."), 400
        renglon = {
            "numero_de_producto": datos["numero_de_producto"],
            "nombre_producto": producto[0],
            "cantidad": cantidad,
            "monto_total": float(producto[1] * cantidad),
        }
        CARRITOS.setdefault(datos.get("id_carrito"), []).append(renglon)
        return jsonify(renglon), 201

    registrar_pedidos(app, CARRITOS.get, lambda id_carrito: CARRITOS.pop(id_carrito, None))
    # Sin modo debug por defecto: en Codespaces el puerto queda público y el depurador
    # de Flask permitiría ejecutar código. Actívalo solo en tu máquina con MYKO_DEBUG=1.
    app.run(port=5000, debug=os.environ.get("MYKO_DEBUG") == "1")
