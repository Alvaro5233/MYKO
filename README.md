# MYKO

Landing y tienda de MYKO, hongos funcionales (Melena de León) cultivados en México.

- **App en línea (con checkout):** https://myko-25t0.onrender.com. La primera visita puede tardar ~50 s porque el servicio gratuito "despierta".
- **Copia estática:** https://alvaro5233.github.io/MYKO/
- **Bitácora del Assignment 2:** [PROMPT_LOG.md](PROMPT_LOG.md)

## Qué hace
1. Agregas productos al carrito con la cantidad que quieras.
2. Capturas tus datos de envío. Al escribir el código postal, la app sugiere el estado y las colonias (API pública Zippopotam.us).
3. El servidor valida los datos con [`esquema_envio.json`](esquema_envio.json) y marca cada error en español.
4. Si todo está bien, simula el pago y guarda el pedido en SQLite.

## Correrlo en tu computadora
```
pip install -r requirements.txt
python app.py
```
Abre http://localhost:5000.

## Archivos
| Archivo | Para qué |
|---|---|
| `index.html` | Página, carrito y checkout |
| `aviso-privacidad.html` | Aviso de privacidad (borrador) |
| `esquema_envio.json` | Reglas de validación del pedido |
| `pedidos.py` | `POST /pedidos` y `GET /codigo-postal/<cp>` |
| `app.py` | App de Flask que se publica en Render |
| `render.yaml`, `requirements.txt` | Configuración del deploy |

## Decisiones de diseño vs. sugerencias del IS

IS = sistema inteligente (Claude Code). Cada entrada dice qué propuso, qué decidí yo y por qué, y cómo lo verifiqué. El detalle completo de cada una está en [PROMPT_LOG.md](PROMPT_LOG.md) (D1 a D11).

### 1. Escalabilidad y seguridad: dónde viven los datos (Sesión 22 + D8)
- **Propuesta del IS:**
  - D8: arrancar con `gunicorn` con varios *workers*, que es lo típico en producción.
  - S22: el diagnóstico dijo que mi cuello de botella es la arquitectura. Para guardar pedidos de verdad propuso pagar Render Starter ($7 al mes) más una base de datos persistente.
- **Mi decisión:**
  - Dejé **1 worker** (`--workers 1 --threads 4` en `render.yaml`).
  - **No pago** el plan Starter por ahora.
  - Documenté el límite y no lo escondí.
- **Motivo:**
  - Con varios workers, el carrito en memoria queda en un proceso y el pedido llega a otro, que responde "Tu carrito está vacío" al azar.
  - En S22 hice la cuenta del tráfico: cada visita descarga ~60 KB (`index.html` pesa 58,817 bytes). Con 1,000× mis usuarios (30,000 visitas al mes) uso 1.8 GB, el 36 % de los 5 GB gratis de Render, y pago $0. O sea, el costo y el tráfico no son el problema.
  - El problema es que Render gratis tiene disco efímero y apaga el servicio tras 15 min sin tráfico ([render.com/docs/free](https://render.com/docs/free)). Por eso SQLite y el carrito se borran.
  - Hoy hay 0 compras reales, así que pagar $7 al mes no protege a ningún cliente todavía.
  - El siguiente paso, cuando haya ventas, es separar el acceso a datos de `pedidos.py` para mover pedidos y carrito a una base persistente.
- **Verificación:**
  - El 18/11, el Caso A del Assignment 2 creó el pedido #1. El 25/11 hice un pedido nuevo contra Render y **volvió a ser el #1**. La base se borró, tal como predijo el diagnóstico.
  - `curl https://myko-25t0.onrender.com/myko.db` sigue dando 404, así que los datos de clientes no se publican (D7).

### 2. Seguridad: la validación vive en el servidor (D1) y solo se publican 2 páginas (D7)
- **Propuesta del IS:**
  - Como `carrito.py` no estaba en la carpeta, ofreció validar el formulario con el esquema **solo en el navegador** y simular el pedido sin backend.
  - Además, la forma rápida de servir el sitio desde Flask era publicar toda la carpeta.
- **Mi decisión:**
  - Rechacé la validación solo en el frontend y pedí un backend (`pedidos.py` con Flask y jsonschema).
  - En `app.py` solo se sirven `index.html` y `aviso-privacidad.html`.
- **Motivo:**
  - Una validación en el navegador se salta con una petición directa con `curl`.
  - Publicar la carpeta expondría `myko.db`, con nombres, teléfonos y direcciones.
  - También pedí quitar `debug=True` (D5), porque el depurador de Flask en un puerto público permite ejecutar código.
- **Verificación:**
  - El Caso B, mandado directo al servidor con `curl`, regresa 422 con un error en cada uno de los 3 campos malos.
  - `/myko.db` y `/pedidos.py` responden 404.

### 3. Deployment: rechacé GitHub Pages como deploy de la función (D6)
- **Propuesta del IS:** publicar en GitHub Pages, donde ya estaba la landing.
- **Mi decisión:** Render, con Flask sirviendo la página y la API desde el mismo origen. La copia de Pages se queda, pero llama a la API de Render.
- **Motivo:**
  - Pages solo sirve archivos estáticos: en el link público, "Agregar al carrito" fallaba y el checkout no se podía probar.
  - En S22 confirmé además que los términos de GitHub Pages prohíben usarlo como tienda en línea ([github-pages-limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
- **Verificación:** commit `Servir página y API desde Flask en Render: Pages no ejecuta Python`. Los casos A a D corren contra https://myko-25t0.onrender.com.

### 4. Funcionalidad: errores que encontré yo y que el IS no señaló (D9 y D11)
- **Propuesta del IS:**
  - Mapear el estado del código postal por **abreviatura**, que parecía lo más limpio.
  - Su código del checkout tenía un `409` para pedidos repetidos, pero nunca se alcanzaba.
- **Mi decisión:**
  - Exigí probar la API con códigos postales reales antes de integrarla. Para `25000` (Saltillo, Coahuila), la API manda `CHP`, que es Chiapas. Cambié el mapeo a **nombre normalizado**.
  - Al correr mi Caso C, el pedido repetido daba `400 "Tu carrito está vacío"` y no `409`. Pedí revisar primero si el carrito ya tenía pedido.
- **Motivo:**
  - Con la abreviatura, los pedidos de Saltillo se habrían ido a Chiapas sin ningún error visible.
  - Con el `400`, a un cliente que da doble clic se le diría que su carrito está vacío justo después de comprar.
- **Verificación:** `25000 → Coahuila` (Caso D). El pedido repetido ahora da `409` (Caso C).
