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
