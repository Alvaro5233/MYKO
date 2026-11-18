# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Landing page and storefront for MYKO, a Mexican functional-mushroom brand (Melena de León / *Hericium erinaceus*). All user-facing copy is in Spanish (`lang="es"`), and so are JS identifiers and comments (`abrirCarrito`, `pintarCarrito`, `mostrarFeedback`). Keep new code and copy in Spanish to match.

The folder is the git repo `Alvaro5233/MYKO` (GitHub). There is no build system, linter or test suite; `PROMPT_LOG.md` records the manual test cases.

## Running

Files:
- `index.html`: the page, with inline `<style>`, inline `<script>`, inline SVG and no external dependencies.
- `aviso-privacidad.html`: privacy notice. It is a **draft pending legal review**, and its `[pendiente]` placeholders still need real data.
- `esquema_envio.json`: JSON Schema (draft 2020-12) for the order and shipping data. It is the single source of truth for validation (and for the list of states).
- `pedidos.py`: Flask blueprint with `POST /pedidos` (validates with the schema via `jsonschema`, simulates payment, saves to SQLite `myko.db`, created automatically) and `GET /codigo-postal/<cp>`.
- `app.py`: the Flask app that is deployed. It serves `index.html` and `aviso-privacidad.html` (only those; never `static_folder="."`, which would expose `myko.db`), the in-memory demo cart `/carrito/agregar` (catalog 101/102) and registers `pedidos.py`.
- `requirements.txt`, `render.yaml`: deploy on Render free tier with `gunicorn app:app --workers 1`. **Keep one worker**: the demo cart lives in process memory. Render's free disk is ephemeral, so `myko.db` resets on each restart/deploy.
- `PROMPT_LOG.md`: course prompt log (spec, accept/reject/revise decisions, validation).

Run locally: `pip install -r requirements.txt` then `python app.py` (or `python pedidos.py`), and open `http://localhost:5000`.

`API_BASE` (top of the `<script>`) is `""` (same origin) when served by Flask, the Render URL (`URL_RENDER`) when the page is opened from GitHub Pages, and `http://localhost:5000` from `file://` or port 8000.

The real cart backend, `carrito.py`, is **not in this repo**; `app.py` stands in for it. To connect orders to it, add after creating `app`:

```python
from pedidos import registrar_pedidos
registrar_pedidos(app, obtener_carrito)  # optional 3rd argument: vaciar_carrito(id_carrito)
```

`obtener_carrito(id_carrito)` returns the cart rows `{numero_de_producto, nombre_producto, cantidad, monto_total}`. CORS must allow `/pedidos` and `/codigo-postal/*`.

**Postal code lookup.** `GET /codigo-postal/<cp>` calls Zippopotam.us (`urllib`, 4 s timeout, in-memory cache) and returns `{codigo_postal, estado, colonias}`, `404` for unknown CPs, `502` if the API fails. The state is mapped **by normalized name** to the schema enum (`_ALIAS_ESTADO` handles "Distrito Federal", "Mexico", etc.). Never map by abbreviation: the API returns `CHP` (Chiapas) for Coahuila. The lookup only pre-fills `estado` and a `<datalist>` of colonias in the form; it must never block or validate an order.

## Architecture

**Cart / backend contract.** The backend is the source of truth for the cart, and the local `carrito` array only renders the side panel.
- Request body: `{ id_carrito, codigo_de_cliente, numero_de_producto, cantidad }`. There is no login yet, so `id_carrito` and `codigo_de_cliente` are random integers (≥100000). They are kept in `sessionStorage` (`myko_sesion`, along with `myko_carrito`) so a reload doesn't lose the cart.
- `cantidad` comes from the quantity selector in each card (`.qty`, `[data-cantidad]`, 1–10).
- A successful response is pushed into `carrito` as-is. `pintarCarrito()` groups rows by `nombre_producto`, adds up `cantidad` and `Number(monto_total)`, and builds the DOM with `textContent` (never `innerHTML` with backend data). The badge shows the number of items.
- Error responses are JSON with an `error` field. `pedirJSON()` tells a network failure apart from a non-JSON response.
- Product cards declare `data-producto-id` (sent as `numero_de_producto`), `data-producto-nombre` and `data-producto-precio`. Only the id is sent today. Current IDs: 101 (cápsulas) and 102 (polvo).

**Checkout.** The side panel has three views (`#vista-carrito`, `#vista-envio`, `#vista-confirmacion`), switched with `mostrarVista()`. The `#form-envio` form mirrors the schema with HTML attributes for UX only, and the server has the final say:
- Body: `{ id_carrito, codigo_de_cliente, acepta_aviso_privacidad: true, envio: {...} }`.
- `422` → `{ error, errores: { campo: mensaje } }`, rendered by `mostrarErroresCampo()` into `[data-error-for="campo"]`. Messages are in Spanish, and the same text appears in `MENSAJES_CAMPO` in both `pedidos.py` and `index.html`.
- `201` → `{ numero_pedido, total, estado_pago, referencia_pago }`. Payment is simulated in `simular_pago()`; the real provider goes there. MYKO never receives card data. The total is computed on the server from `obtener_carrito`.
- `409` if that `id_carrito` already has an order (checked before the empty-cart `400`, since the cart is emptied after an order). After an order is confirmed, the frontend generates a new `idCarrito`.
- If you add a field: update `esquema_envio.json`, the form, `MENSAJES_CAMPO` (both files), `CAMPOS_TEXTO` and the `pedidos` table. `CREATE TABLE IF NOT EXISTS` doesn't migrate an existing `myko.db`.

**Styling.** All colors and fonts are CSS custom properties on `:root` (`--ink`, `--paper`, `--green`, etc.). Use these tokens instead of hard-coded colors (errors use `--error`). A global `[hidden]{display:none !important}` rule makes the `hidden` attribute work on elements that set `display`. The page alternates dark (`--ink` background) and light (`--paper` / `--paper-alt`) sections, and per-element accent colors use local custom properties set with `:nth-child` (`--card-accent`, `--col-accent`). Responsive breakpoints are at 900px and 520px, collected at the end of the stylesheet. Animations respect `prefers-reduced-motion`.

**Content constraints.** The "Ciencia" section deliberately avoids medical or health claims, and includes a disclaimer that MYKO does not cure, treat or prevent disease. New copy should keep that cautious, evidence-honest tone.
