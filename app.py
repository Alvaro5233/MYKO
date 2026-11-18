"""
App de MYKO para deploy (Render) y para correr en local.

Sirve la página y la API desde el mismo origen:
  GET  /                      index.html
  GET  /aviso-privacidad.html aviso de privacidad
  POST /carrito/agregar       carrito de prueba en memoria (mientras no exista carrito.py)
  POST /pedidos               valida, simula el pago y guarda el pedido (pedidos.py)
  GET  /codigo-postal/<cp>    estado y colonias de un CP (API externa, ver pedidos.py)

Local:   pip install -r requirements.txt  y  python app.py   (http://localhost:5000)
Render:  gunicorn app:app --workers 1 --threads 4   (ver render.yaml)

Importante: el carrito vive en la memoria del proceso, por eso en producción se usa
UN solo worker. Con varios, el producto se agrega en un proceso y el pedido llega a
otro que no lo conoce ("Tu carrito está vacío").
"""

import os

from flask import Flask, jsonify, request, send_from_directory

from pedidos import CARPETA, registrar_pedidos

app = Flask(__name__)

CATALOGO = {
    101: ("Cápsulas Melena de León", 300),
    102: ("Polvo Melena de León", 300),
}
CARRITOS = {}  # id_carrito -> lista de renglones, solo en memoria

# Solo estas páginas se sirven. No usamos static_folder="." porque expondría
# pedidos.py, esquema_envio.json y myko.db (datos de envío de clientes).
PAGINAS_PUBLICAS = {"index.html", "aviso-privacidad.html"}


@app.after_request
def permitir_cors(respuesta):
    # Permite que la copia de la página en GitHub Pages use esta API.
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    respuesta.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return respuesta


@app.route("/")
def inicio():
    return send_from_directory(CARPETA, "index.html")


@app.route("/<pagina>")
def pagina(pagina):
    if pagina not in PAGINAS_PUBLICAS:
        return jsonify(error="No encontrado."), 404
    return send_from_directory(CARPETA, pagina)


@app.route("/carrito/agregar", methods=["POST"])
def agregar():
    datos = request.get_json(silent=True) or {}
    producto = CATALOGO.get(datos.get("numero_de_producto"))
    cantidad = datos.get("cantidad")
    if not producto:
        return jsonify(error="Producto no encontrado."), 404
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or not 1 <= cantidad <= 10:
        return jsonify(error="La cantidad debe ser de 1 a 10."), 400
    renglon = {
        "numero_de_producto": datos["numero_de_producto"],
        "nombre_producto": producto[0],
        "cantidad": cantidad,
        # El precio sale del catálogo del servidor, nunca del navegador.
        "monto_total": float(producto[1] * cantidad),
    }
    CARRITOS.setdefault(datos.get("id_carrito"), []).append(renglon)
    return jsonify(renglon), 201


registrar_pedidos(app, CARRITOS.get, lambda id_carrito: CARRITOS.pop(id_carrito, None))


if __name__ == "__main__":
    # Sin modo debug por defecto: si el puerto queda público, el depurador de Flask
    # permitiría ejecutar código. Actívalo solo en tu máquina con MYKO_DEBUG=1.
    app.run(port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("MYKO_DEBUG") == "1")
