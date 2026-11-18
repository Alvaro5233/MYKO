# Bitácora de prompts: Assignment 2 · MYKO

**Función:** checkout con datos de envío validados por un esquema JSON, con pedido guardado en base de datos y sugerencia de estado y colonias por código postal (API externa).
**Alumno:** Álvaro (GitHub `Alvaro5233`)
**Herramienta de IA:** Claude Code (CLI), en el repositorio del proyecto.

| Pieza | Link |
|---|---|
| Deploy con la función (Render) | https://myko-25t0.onrender.com |
| Copia estática (GitHub Pages, usa la API de Render) | https://alvaro5233.github.io/MYKO/ |
| Repositorio | https://github.com/Alvaro5233/MYKO |

> Nota sobre el deploy: el plan gratis de Render "duerme" el servicio después de 15 min sin uso. La primera visita puede tardar ~50 s en responder.

---

## Contexto: qué no podía hacer la app antes

En Assignment 1 MYKO era una landing con productos y un carrito que solo agregaba piezas. **No había forma de cerrar una compra**: no se pedían datos de envío, nada se validaba y no se guardaba ningún pedido. Esta entrega agrega ese paso, con datos reales que viajan al servidor, se validan contra un esquema y se guardan en SQLite. También agrega una integración con una API pública de códigos postales.

---

## Paso 1: Especificar (Checkpoint A)

### 1.1 Versión original (prompt que le di a la IA el 4 de noviembre)

> **Qué hace y para quién:** cuando el cliente de MYKO termina de agregar productos al carrito, la app le pide sus datos de envío y revisa con un esquema JSON que estén completos y bien escritos (código postal, teléfono, ciudad, estado) antes de crear el pedido. Hoy el carrito guarda productos pero no cierra la compra.
>
> **De dónde salen los datos:** el carrito y el catálogo con precios ya los guarda mi app (carrito.py). Los datos de envío los escribe el usuario y la app los guarda en su propia base de datos. El pago no lo guardamos nosotros: lo haría un proveedor de pagos externo, y en esta etapa se simula.
>
> ¿Para quién es y qué problema le quita? Para los clientes y lo que soluciona es hacer pedidos de forma simple, segura y rápida. · ¿Necesita clave o permiso? Necesito un aviso de privacidad para utilizar los datos del usuario. · ¿Dónde va? En la esquina superior derecha estará el carrito y para agregar un producto va a tener la opción debajo del producto y la cantidad.

### 1.2 Auditoría

En la Sesión 19 trabajé en pareja con **Brandon**, pero la auditoría en vivo la hicimos sobre **su** proyecto. Para auditar la especificación de MYKO le pedí a la IA que actuara como el compañero auditor y cuestionara cada campo vago. Lo que señaló y lo que decidí:

| Campo | Cuestionamiento | Mi decisión |
|---|---|---|
| Qué hace | "Bien escritos" no dice qué es correcto. ¿Un CP de 4 dígitos es error? ¿"CDMX" es un estado válido? | **Acepto.** Defino reglas exactas por campo (abajo) y una lista cerrada de 32 estados. |
| Qué hace | "Simple, segura y rápida" no se puede verificar. | **Acepto.** Lo quito del campo y lo convierto en criterios medibles (mensajes por campo, sin datos de tarjeta, total calculado en el servidor). |
| Datos | "Todos los datos son del cliente mediante un JSON" contradice lo anterior: el **precio** no debe venir del cliente. | **Acepto.** Separo las fuentes: producto y cantidad = cliente; precio = catálogo del servidor; envío = formulario. |
| Datos | No dice qué pasa con el pago ni qué se guarda. | **Acepto.** Pago simulado; no se pide ni se guarda ningún dato de tarjeta. |
| Cómo se sabrá | No existía este campo. | **Acepto.** Agrego 4 casos de prueba con resultado esperado exacto. |

### 1.3 Especificación final (3 campos)

**1. Qué hace.** Cuando el cliente tiene productos en el carrito y presiona "Continuar con el envío", la app muestra un formulario de envío. Al confirmar, el servidor valida los datos contra `esquema_envio.json`:
- nombre: 3 a 80 caracteres, solo letras;
- teléfono: 10 dígitos;
- correo válido;
- calle, número y colonia obligatorios;
- código postal: 5 dígitos;
- ciudad: solo letras;
- estado: uno de los 32 de la lista;
- aceptación obligatoria del aviso de privacidad.

Si hay errores, responde con un mensaje en español **por campo**. Si los datos son válidos, simula el pago, guarda el pedido en SQLite y responde con número de pedido, total y referencia de pago. Extensión: al escribir el código postal, la app sugiere el estado y las colonias consultando una API pública.

**2. Qué datos necesita y de dónde vienen.**
- `id_carrito` y `codigo_de_cliente`: ya existen en la app (se generan al abrir la página y viven en `sessionStorage`).
- Productos, cantidades y **precios**: el carrito del servidor (`/carrito/agregar`) con el catálogo del servidor (101 cápsulas, 102 polvo, $300 c/u). El navegador nunca manda precios.
- Datos de envío (nombre, teléfono, correo, calle, número exterior e interior, colonia, CP, ciudad, estado, referencias): los escribe el cliente en un formulario nuevo.
- Aceptación del aviso de privacidad: casilla nueva, enlazada a `aviso-privacidad.html`.
- Estado y colonias sugeridos: API externa `api.zippopotam.us/mx/{cp}` (pública, sin clave).

**3. Cómo se sabrá que funciona (criterio verificable).**
- **Caso A (pedido válido):** carrito con cápsulas ×2 y polvo ×1, datos completos → `201`, `total: 900.0`, `estado_pago: "aprobado"`, referencia `SIM-…`.
- **Caso B (datos inválidos):** CP `1234`, teléfono `55123`, estado `Distrito Federal` → `422` con un mensaje en español en **cada uno de esos 3 campos**, sin crear pedido.
- **Caso C (casos límite):** mismo carrito dos veces → `409`; carrito vacío → `400`; sin aceptar el aviso → `422` en `acepta_aviso_privacidad`.
- **Caso D (API externa):** CP `06700` → estado `Ciudad de México`; CP `25000` → `Coahuila`; CP inexistente → `404`. Si la API falla, el pedido **se puede hacer igual**.

---

## Paso 2: Construir. Registro de aceptar / rechazar / revisar

Cada entrada dice qué propuso la IA, qué campo de mi especificación estaba en juego, qué decidí y por qué.

### Prompt inicial (referencia a la especificación)
> "Vamos a agregar una función al proyecto… [especificación 1.1 completa] … el código de la página está en los archivos de la carpeta y no estoy seguro de que funcione bien el carrito, también checa eso."

### D1 · Dónde vive la validación: **Rechazo** la opción "solo frontend"
- **Propuesta de la IA:** como `carrito.py` no estaba en la carpeta, ofreció tres opciones. Una era *"hago el formulario y la validación con el esquema en el navegador, y el pedido se simula sin backend"*.
- **Campo en juego:** *Datos* ("la app los guarda en su propia base de datos") y *Qué hace* (el servidor crea el pedido).
- **Decisión:** rechazada. Elegí un backend nuevo (`pedidos.py`, Flask + jsonschema). Una validación solo en el navegador se salta con una petición directa, y sin backend no hay base de datos. Esto contradecía mi especificación.

### D2 · Base de datos: **Acepto** SQLite y **rechazo** un archivo JSON
- **Propuesta de la IA:** SQLite, la misma base que carrito.py, o "guardar los pedidos en un pedidos.json, lo más simple posible".
- **Campo en juego:** *Datos* (base de datos propia).
- **Decisión:** SQLite. Un archivo JSON no evita que dos pedidos simultáneos se pisen y no permite la restricción "un pedido por carrito" (`UNIQUE id_carrito`), que necesito para el Caso C.

### D3 · De dónde sale el total: **Acepto, con condición**
- **Propuesta de la IA:** calcular el total en el servidor con `obtener_carrito()` en vez de con lo que mande el navegador.
- **Campo en juego:** *Datos*, en la fuente del precio (lo corregí en la auditoría: el precio no viene del cliente).
- **Decisión:** aceptada. Además verifiqué que la página no mande precio al servidor: `data-producto-precio` existe en el HTML, pero solo se envía `numero_de_producto` y `cantidad`.

### D4 · Alcance: **Reviso** los arreglos extra del carrito
- **Propuesta de la IA:** al revisar el carrito encontró 8 problemas y propuso corregirlos todos:
  1. siempre mandaba `cantidad: 1`;
  2. el mismo producto salía en filas duplicadas;
  3. había riesgo de XSS por usar `innerHTML` con datos del servidor;
  4. fallaba si `monto_total` llegaba como texto;
  5. un error raro del servidor se reportaba como "no se pudo conectar";
  6. al recargar se perdía el carrito;
  7. no había botón para continuar la compra;
  8. la fila "Total" nunca se ocultaba.
- **Campo en juego:** *Qué hace*, que exige que el cliente "termine de agregar productos al carrito" con la cantidad elegida.
- **Decisión:** acepté los 8 porque yo pedí revisar el carrito y el punto 1 contradecía directamente mi especificación ("la opción debajo del producto **y la cantidad**"). **Dejé fuera** "quitar productos del carrito": no está en mi especificación y requiere una ruta nueva en el carrito del servidor.

### D5 · Seguridad del servidor: **Pido revisión** del modo debug
- **Propuesta de la IA:** la primera versión arrancaba con `app.run(debug=True)`.
- **Campo en juego:** *Qué hace* (pedido "seguro") y *Datos* (datos personales de envío).
- **Decisión:** revisado. Al exponer el servidor en un puerto público, el depurador de Flask permite ejecutar código. Ahora arranca sin debug; solo se activa en mi máquina con `MYKO_DEBUG=1`.

### D6 · Dónde se publica: **Rechazo** GitHub Pages como deploy de la función
- **Propuesta de la IA:** publicar la página en GitHub Pages. Ya estaba publicada en https://alvaro5233.github.io/MYKO/.
- **Campo en juego:** *Cómo se sabrá que funciona*, porque los casos A a D tienen que poder correrse contra el deploy.
- **Decisión:** rechazado como deploy principal. Pages solo sirve archivos estáticos y la página llamaba a `http://localhost:5000`, así que en el link público "Agregar al carrito" fallaba y el checkout no era verificable. Pedí una alternativa: `app.py` sirve la página y la API desde el mismo origen en **Render**. La copia de Pages se queda, pero apunta a la API de Render. Commit: `Servir página y API desde Flask en Render: Pages no ejecuta Python`.

### D7 · Qué archivos se publican: **Reviso** la forma de servir la página
- **Situación:** la forma rápida de servir el sitio desde Flask es publicar toda la carpeta como estática.
- **Campo en juego:** *Datos*, porque los datos de envío viven en `myko.db`, en la misma carpeta.
- **Decisión:** solo se sirven `index.html` y `aviso-privacidad.html`. Publicar la carpeta expondría `myko.db` (nombres, teléfonos y direcciones de clientes) y el código del servidor. Lo verifiqué con la prueba 7 del Paso 3.

### D8 · Número de procesos en producción: **Reviso** el comando de arranque
- **Situación:** el arranque típico de Flask en producción es `gunicorn` con varios *workers*.
- **Campo en juego:** *Datos*. El carrito de prueba vive en la memoria del proceso. Con varios workers, el producto se agrega en un proceso y el pedido llega a otro que no lo conoce: el Caso A fallaría con "Tu carrito está vacío" de forma aleatoria.
- **Decisión:** `--workers 1 --threads 4` (en `render.yaml`), documentado en `app.py`.

### D9 · API de códigos postales: **Corrijo** el mapeo de estados (error de datos de la API)
- **Situación:** antes de integrar la API pedí probarla con CPs reales (lo que vimos en la S16: verificar la API contra su respuesta real, no contra lo que uno supone).
- **Hallazgo 1:** los nombres de estado de la API **no coinciden** con mi esquema: `06700 → "Distrito Federal"`, `50000 → "Mexico"`, `58000 → "Michoacan De Ocampo"`, `91000 → "Veracruz Llave"`, `76000 → "Queretaro De Arteaga"`. Si se copiaran tal cual al formulario, el servidor rechazaría el pedido (Caso B).
- **Hallazgo 2, el más grave:** para `25000` (Saltillo, Coahuila) la API responde `"state abbreviation": "CHP"`, que es la abreviatura de **Chiapas**. Mapear por abreviatura, que parece lo más limpio, habría mandado a Chiapas los pedidos de Saltillo **sin ningún error visible**.
- **Campo en juego:** *Cómo se sabrá que funciona*, Caso D (`25000 → Coahuila`).
- **Decisión:** mapear por **nombre normalizado** (sin acentos, minúsculas) contra la lista de estados que se lee de `esquema_envio.json`, que sigue siendo la única fuente de verdad, más una tabla de alias para los nombres oficiales y viejos. Commit: `Sugerir estado y colonias por código postal; mapear estado por nombre`.

### D10 · Rol de la API externa: **Rechazo** usarla para validar
- **Alternativa considerada:** usar la API para *validar* que el CP corresponda al estado y rechazar el pedido si no coinciden.
- **Campo en juego:** *Cómo se sabrá que funciona*, Caso D ("si la API falla, el pedido se puede hacer igual").
- **Decisión:** rechazado. La API es un servicio gratuito de terceros que puede caerse o tener datos malos (D9 lo demuestra). Si validara, una caída suya impediría vender. La API solo **sugiere**: preselecciona el estado y llena una lista de colonias, y el cliente puede cambiar todo. Si responde 404 o 502, el formulario sigue funcionando a mano.

### D11 · Error encontrado en mis pruebas: **Corrijo** el mensaje de pedido repetido
- **Situación:** al correr el Caso C en local, enviar dos veces el mismo carrito respondió:
  ```
  {"error":"Tu carrito está vacío."}
  HTTP 400
  ```
  y no el `409` que pide mi especificación. La IA no lo había señalado. El código sí tenía un `409`, pero era inalcanzable: después del primer pedido el carrito se vacía, así que el segundo intento caía antes en "carrito vacío".
- **Campo en juego:** *Cómo se sabrá que funciona*, Caso C (mismo carrito dos veces → `409`).
- **Decisión:** el servidor revisa primero si el carrito ya tiene pedido. No era un pedido duplicado (no se cobraba dos veces), pero el mensaje engañaba: a un cliente que da doble clic le diría que su carrito está vacío justo después de comprar. Volví a correr la prueba (resultado en el Paso 3).

---

## Paso 3: Validar contra el deploy

Pruebas corridas con `curl` contra **https://myko-25t0.onrender.com** el 17 de noviembre de 2026 (05:20 UTC del 18). Los outputs están copiados tal cual: los acentos aparecen como `á` porque así los codifica JSON. Cada cuerpo se mandó desde un archivo UTF-8 (`--data-binary @cuerpo.json`), igual que lo hace el navegador.

**Deploy confirmado:**
```
$ curl -s https://myko-25t0.onrender.com/ | grep -o '<title>.*</title>'
<title>MYKO — Hongos funcionales, cultivados por nosotros</title>
HTTP 200
```

### Caso A: pedido válido (caso principal)
**Input exacto:**
```
POST /carrito/agregar  {"id_carrito":931128,"codigo_de_cliente":122570,"numero_de_producto":101,"cantidad":2}
POST /carrito/agregar  {"id_carrito":931128,"codigo_de_cliente":122570,"numero_de_producto":102,"cantidad":1}
POST /pedidos          {"id_carrito":931128,"codigo_de_cliente":122570,"acepta_aviso_privacidad":true,"envio":{"nombre_completo":"Ana López Ruiz","telefono":"55 1234 5678","correo":"ana@example.com","calle":"Av. Álvaro Obregón","numero_exterior":"120","colonia":"Roma Norte","codigo_postal":"06700","ciudad":"Cuauhtémoc","estado":"Ciudad de México"}}
```
**Output real:**
```
{"cantidad":2,"monto_total":600.0,"nombre_producto":"Cápsulas Melena de León","numero_de_producto":101}
HTTP 201
{"cantidad":1,"monto_total":300.0,"nombre_producto":"Polvo Melena de León","numero_de_producto":102}
HTTP 201
{"estado_pago":"aprobado","numero_pedido":1,"referencia_pago":"SIM-7E826E5C09","total":900.0}
HTTP 201
```
**Veredicto: ACEPTAR.** Respondió `HTTP 201` con `"total":900.0`, igual a 600.0 + 300.0, que el servidor calculó con su catálogo. Además `"estado_pago":"aprobado"` y `"referencia_pago":"SIM-7E826E5C09"`, como pide el Caso A. El teléfono se mandó con espacios (`"55 1234 5678"`) y aun así se aceptó, porque el servidor lo normaliza antes de validar.

### Caso B: datos inválidos
**Input exacto:**
```
POST /pedidos  {"id_carrito":931129,"codigo_de_cliente":122570,"acepta_aviso_privacidad":true,"envio":{"nombre_completo":"Ana López Ruiz","telefono":"55123","correo":"ana@example.com","calle":"Av. Álvaro Obregón","numero_exterior":"120","colonia":"Roma Norte","codigo_postal":"1234","ciudad":"Cuauhtémoc","estado":"Distrito Federal"}}
```
**Output real:**
```
{"error":"Revisa los datos de envío.","errores":{"codigo_postal":"El código postal debe tener 5 dígitos.","estado":"Elige un estado de la lista.","telefono":"El teléfono debe tener 10 dígitos."}}
HTTP 422
```
**Veredicto: ACEPTAR.** `errores` trae exactamente las 3 claves del input malo (`codigo_postal`, `estado`, `telefono`), cada una con su mensaje en español, y ninguna de los 6 campos correctos. `"Distrito Federal"` se rechazó con "Elige un estado de la lista.", lo que confirma por qué la API de CP necesitaba el mapeo de D9.

### Caso C: casos límite
**Input y output reales:**
```
# Mismo carrito 931128 del Caso A, mismo cuerpo, segunda vez:
{"error":"Este carrito ya tiene un pedido."}
HTTP 409

# Carrito 931130, al que nunca se le agregó nada:
{"error":"Tu carrito está vacío."}
HTTP 400

# Carrito 931131 con "acepta_aviso_privacidad":false (resto igual al Caso A):
{"error":"Revisa los datos de envío.","errores":{"acepta_aviso_privacidad":"Debes aceptar el aviso de privacidad."}}
HTTP 422
```
**Veredicto: ACEPTAR**, después de una revisión. El pedido repetido ahora da `HTTP 409` con `"Este carrito ya tiene un pedido."`. En la primera corrida (en local, antes de D11) daba `HTTP 400` con `"Tu carrito está vacío."`, así que **inicialmente el veredicto fue REVISAR**. Ya corregido, los tres códigos (409, 400 y 422) coinciden con el Caso C.

### Caso D: API externa de códigos postales
**Input y output reales:**
```
$ curl -s https://myko-25t0.onrender.com/codigo-postal/25000
{"codigo_postal":"25000","colonias":["Saltillo Centro"],"estado":"Coahuila"}
HTTP 200

$ curl -s https://myko-25t0.onrender.com/codigo-postal/06700
{"codigo_postal":"06700","colonias":["Roma Norte"],"estado":"Ciudad de México"}
HTTP 200

$ curl -s https://myko-25t0.onrender.com/codigo-postal/00000
{"error":"No encontramos ese código postal."}
HTTP 404
```
**Veredicto: ACEPTAR.** Para `25000` respondió `"estado":"Coahuila"` aunque la API original manda la abreviatura `CHP`, de Chiapas (D9). Para `06700` respondió `"Ciudad de México"` en vez del `"Distrito Federal"` de la API, que es el valor que el esquema sí acepta. Un CP inexistente da `404` con un mensaje, no un error del servidor.

### Prueba extra: datos privados no expuestos (D7)
```
$ curl -s https://myko-25t0.onrender.com/myko.db
{"error":"No encontrado."}
HTTP 404
```
**Veredicto: ACEPTAR.** La base con los datos de envío no se puede descargar desde el deploy.

### Prueba en el navegador
En https://myko-25t0.onrender.com agregué productos, escribí el CP `06700` y el estado se llenó solo con "Ciudad de México". Llené el formulario, acepté el aviso y apareció "Pedido #… confirmado".

---

## Por qué la función resuelve el problema

El problema de la especificación era: *"Hoy el carrito guarda productos pero no cierra la compra"*. Con la evidencia del Paso 3:
- **Cierra la compra.** El Caso A crea un pedido real con número y referencia, guardado en SQLite.
- **"Completos y bien escritos" ya es verificable.** El Caso B muestra que los tres errores del input (CP, teléfono, estado) se detectan **a la vez**, con un mensaje en español en cada campo. No es un solo "error" genérico, así que el cliente sabe exactamente qué corregir.
- **Los datos vienen de donde dice la especificación.** El total ($900) lo calculó el servidor con su catálogo (D3). La página no manda precios.
- **Es seguro con los datos personales.** Es obligatorio aceptar el aviso de privacidad (Caso C, 422). `myko.db` no se publica (prueba 7). No se recibe ningún dato de tarjeta.
- **La integración externa ayuda sin volverse un punto de falla.** Corrige el estado a la forma que acepta el esquema (D9) y, si se cae, no bloquea la compra (D10).

### Limitaciones conocidas (documentadas, no ocultas)
- **Pago simulado** (`SIM-…`). El proveedor real se conecta en `simular_pago()`.
- En Render gratis, el disco es temporal: **`myko.db` se borra al reiniciar el servicio**. Para producción hace falta una base de datos administrada (por ejemplo Postgres).
- El carrito del servidor es una versión de prueba en memoria, porque el `carrito.py` original no está en el repositorio. `pedidos.py` ya se conecta a él con dos líneas (`registrar_pedidos(app, obtener_carrito)`).
- El aviso de privacidad es un **borrador** pendiente de revisión legal.
- La API de CP no da la ciudad o municipio, solo estado y colonias, así que la ciudad se escribe a mano.

---

## Uso de IA

- **Herramienta:** Claude Code (Anthropic), usado desde la terminal dentro del repositorio del proyecto.
- **Para qué la usé:**
  - revisar el carrito existente y encontrar sus fallas;
  - generar el esquema JSON, el backend (`pedidos.py`, `app.py`), el formulario y la lógica del checkout;
  - preparar el deploy en Render;
  - actuar como auditor de mi especificación (en clase la auditoría en pareja fue sobre el proyecto de Brandon);
  - ayudarme a redactar esta bitácora.
- **Qué decidí y verifiqué yo:**
  - la función y su especificación;
  - rechacé la validación solo en frontend (D1), el archivo JSON como base de datos (D2) y GitHub Pages como deploy de la función (D6);
  - limité el alcance (D4, sin "quitar productos");
  - decidí que la API de CP solo sugiera y nunca valide (D10);
  - exigí verificar la API con CPs reales antes de integrarla, lo que destapó el error de Coahuila y Chiapas (D9);
  - los casos de prueba (con `curl`, desde la terminal de Claude Code) se corrieron contra mi especificación del Paso 1, y yo revisé cada output contra el resultado esperado. Así salió el 400 que debía ser 409 (D11);
  - hice el flujo completo en el navegador sobre el deploy.
