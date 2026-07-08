# Orion — Stack Django REST + Express BFF + Vue (rama `migracion-django-vue`)

Migración del sitio de Orion (productora de eventos) a un stack de 3 servicios:

```
Vue 3 SPA (Bootstrap, TS)  →  Express BFF (TS)  →  Django REST (DRF)  →  Supabase Postgres
      frontend-vue/               bff-express/         backend-django/
   GitHub Pages (estático)        Render/Railway       Render/Railway
```

- **frontend-vue/** — Vue 3 + TypeScript + Vite + Bootstrap 5. SPA que consume el BFF.
- **bff-express/** — Express + TypeScript. Gateway/proxy fino hacia Django.
- **backend-django/** — Django REST Framework. Único dueño del esquema (ORM) sobre Supabase Postgres.
- **Supabase** se usa solo como base de datos Postgres (sin supabase-js ni RLS; el acceso lo controla el API).

Dominio en **español** (tablas/campos/slugs).

## Requisitos

- **Python 3.12+** (probado con 3.14). En este equipo está en `C:\Users\mateo.araneda\AppData\Local\Programs\Python\Python314`.
- **Node 20+** (en este equipo en `C:\Users\mateo.araneda\node`, ya en PATH).
- Cadena de conexión de **Supabase Postgres** con password.

## Variables de entorno

Cada servicio tiene su `.env.example`. Copiar a `.env` y completar.

### backend-django/.env
```
DATABASE_URL=postgresql://postgres.<ref>:<PASSWORD>@aws-0-<region>.pooler.supabase.com:6543/postgres?sslmode=require
DJANGO_SECRET_KEY=<algo-largo-y-aleatorio>
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3001
ALLOWED_HOSTS=localhost,127.0.0.1
```
La cadena se obtiene en Supabase → **Settings → Database → Connection string → URI** (usar el **pooler**, puerto 6543).

### bff-express/.env
```
DJANGO_API_URL=http://localhost:8000
PORT=3001
ALLOWED_ORIGINS=http://localhost:5173,https://rektres.github.io
```

### frontend-vue/.env
```
VITE_API_URL=http://localhost:3001/api
VITE_WHATSAPP_NUMBER=56944830378
VITE_BASE=/
```

## Levantar en local (3 terminales)

### 1. Django (API de datos) — puerto 8000
```bash
cd backend-django
python -m venv .venv
.venv\Scripts\activate           # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
# Con DATABASE_URL configurado en .env:
python manage.py migrate --fake-initial   # adopta las tablas existentes sin recrearlas
python manage.py runserver 8000
```

### 2. Express BFF — puerto 3001
```bash
cd bff-express
npm install
npm run dev
```

### 3. Vue SPA — puerto 5173
```bash
cd frontend-vue
npm install
npm run dev
```

Abrir **http://localhost:5173**.

## Endpoints del API (Django, bajo `/api/`)

`categorias-servicio/` · `servicios/?categoria=<slug>` · `servicios/<id>/` · `evento-tipos/` · `eventos/?tipo=<slug>&destacado=<bool>` · `eventos/<slug>/` · `eventos/<id>/fotos/` · `posts/?tag=<slug>&limit=&offset=` · `posts/<slug>/` · `tags/` · `POST cotizaciones/`

El BFF expone las mismas rutas en `http://localhost:3001/api/...` (proxy).

## Deploy

- **Vue → GitHub Pages**: build con `VITE_BASE=/OrionProducciones/` y `VITE_API_URL=<URL pública del BFF>`; copiar `dist/index.html` a `404.html`; publicar `frontend-vue/dist`.
- **Django + Express → Render/Railway**: cada uno como servicio web. Variables de entorno (incl. `DATABASE_URL`, secretos) en el panel. `CORS_ALLOWED_ORIGINS`/`ALLOWED_ORIGINS` deben incluir `https://rektres.github.io`. Django en prod con `gunicorn orion_api.wsgi`.

## Notas

- 🔐 `DATABASE_URL` incluye password → solo en `.env` (git-ignored) o en el panel del host. Nunca en el front.
- Django conecta como rol privilegiado ⇒ RLS no protege: cada endpoint de lectura filtra contenido publicado (`activo`/`publicado`/`estado='publicado'`).
- `--fake-initial` adopta las tablas ya existentes en Supabase sin recrearlas (preserva los datos seed).
- El app React original permanece en la rama `main` como referencia.
