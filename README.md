# Orion — sitio de la productora

Sitio web de **Orion**, productora de eventos (Chile). Stack de cuatro servicios en contenedores,
detrás de un Nginx que es el único puerto expuesto:

```
        ┌──────────── docker compose · red orion_net ─────────────┐
        │                                                          │
Navegador ──▶ Nginx :80 ──┬──▶ Frontend Vue 3   (nginx :3000, estáticos)
                          │
                          └──▶ BFF Express :3001 ──▶ Django REST :8000 ──▶ PostgreSQL 16 :5432
                                                            │
                                                            └──▶ SMTP (aviso de cotizaciones)
```

El sitio público es de solo lectura (servicios, portafolio, FAQ) y permite enviar cotizaciones.
El contenido se administra desde `/admin`, un panel dentro de la misma SPA autenticado con token DRF.

Dominio en **español**: tablas, campos y slugs de rutas (`servicios`, `eventos`, `cotizaciones`,
`portafolio/:slug`).

## Tecnologías

| Servicio | Stack |
|---|---|
| `frontend-vue/` | Vue 3 (Composition API, `<script setup>`) · TypeScript strict · Vite 5 · Vue Router 4 · Bootstrap 5 · Axios · DOMPurify |
| `bff-express/` | Node 20 · Express · TypeScript · `http-proxy-middleware` · CORS |
| `backend-django/` | Django 5.1 · Django REST Framework · TokenAuthentication · Pillow · Gunicorn · psycopg 3 |
| Datos | PostgreSQL 16 (contenedor propio, volumen `postgres_data`) |
| Infra | Docker Compose · Nginx (reverse proxy) · systemd · GitHub Actions con runner self-hosted |

Detalles que no se ven en la tabla:

- **Sin storage externo.** Las imágenes se guardan como binario en la tabla `imagenes_archivo`.
  Al subirlas se validan por tamaño, MIME y firma mágica, y se recodifican a **WebP** reescalando a
  1920 px (`catalogo/imagenes.py`). Se sirven por `/api/imagenes/<uuid>/` con cache inmutable.
- **SEO.** `useSeo.ts` escribe title, description, canonical y Open Graph por ruta; las etiquetas
  estáticas de `index.html` cubren a los crawlers que no ejecutan JS. `robots.txt` y `sitemap.xml`
  los genera Django (`catalogo/seo.py`) con los slugs publicados y la URL pública real.
- **Analítica opcional.** Soporta Plausible o GA4 por variable de entorno y viene **apagada**: sin
  configurar no carga ningún script ni cookie de terceros. El banner de consentimiento aparece solo
  con GA4.
- **Tema claro/oscuro** con variables CSS propias (`--orion-*`).

## Estructura

```
backend-django/   API Django REST. App única `catalogo` (modelos, endpoints públicos y admin).
bff-express/      Proxy fino: reenvía /api/* a Django conservando método, headers y multipart.
frontend-vue/     SPA pública + panel /admin.
nginx/            Reverse proxy: "/" → frontend, "/api/" → BFF, "/robots.txt" y "/sitemap.xml" → Django.
.systemd/         Unit para levantar el stack al arranque del servidor.
```

## Levantar en local

Requisitos: **Docker** con Compose v2. Para trabajar servicio por servicio, además Node 20+ y Python 3.12+.

```bash
cp .env.production.example .env    # completar secretos
docker compose up -d --build
```

Queda en **http://localhost**. Logs con `docker compose logs -f`, apagar con `docker compose down`.

### Desarrollo servicio por servicio

```bash
cd backend-django && python -m venv .venv && .venv/Scripts/activate   # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 8000

cd bff-express  && npm install && npm run dev     # :3001
cd frontend-vue && npm install && npm run dev     # :5173
```

Crear el usuario del panel: `python manage.py createsuperuser`.

## Variables de entorno

**Raíz (`.env`)** — la consume `docker compose`. Plantilla completa y comentada en
[`.env.production.example`](./.env.production.example): `DATABASE_URL`, `POSTGRES_PASSWORD`,
`DJANGO_SECRET_KEY`, `DEBUG`, `DB_SSL_REQUIRE`, `SERVER_IP`, `ALLOWED_ORIGINS`, `PG_BIND_IP` y el
bloque SMTP (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`,
`DEFAULT_FROM_EMAIL`, `ADMIN_NOTIFICATION_EMAIL`).

**Frontend (`frontend-vue/.env`)** — ver [`frontend-vue/.env.example`](./frontend-vue/.env.example):
`VITE_API_URL`, `VITE_WHATSAPP_NUMBER`, `VITE_BASE`, redes y contacto del footer
(`VITE_CONTACT_EMAIL`, `VITE_CONTACT_DIRECCION`) y analítica (`VITE_ANALYTICS_PROVIDER`,
`VITE_ANALYTICS_ID`).

En producción `VITE_API_URL` es la ruta relativa `/api`, así que el mismo build sirve para cualquier
IP o dominio sin reconstruir.

## Endpoints (`/api/`)

**Públicos (lectura):** `categorias-servicio/` · `servicios/` · `servicios/<id>/` · `evento-tipos/` ·
`eventos/` · `eventos/<slug>/` · `eventos/<id>/fotos/` · `posts/` · `posts/<slug>/` · `tags/` ·
`imagenes/<uuid>/`

**Público (escritura):** `POST cotizaciones/` — con throttle por IP.

**Panel:** `POST auth/token/` y el CRUD bajo `admin/` (`servicios`, `categorias-servicio`, `eventos`,
`evento-tipos`, `fotos-evento`, `posts`, `tags`), todos con `TokenAuthentication` + `IsAuthenticated`.

**Fuera de `/api/`:** `GET /health` (healthcheck del contenedor) y, expuestos por Nginx en la raíz,
`/robots.txt` y `/sitemap.xml`.

## Verificación antes de commitear

No hay suite de tests. Las mismas puertas que corre el CI:

```bash
cd frontend-vue  && npm run build        # vue-tsc + vite build
cd bff-express   && npm run typecheck
cd backend-django && python manage.py check
cd backend-django && python manage.py makemigrations --check --dry-run
```

## Despliegue

Automático por **GitHub Actions** (`.github/workflows/deploy-docker.yml`) al hacer push a `main` o a
`migracion-django-vue`:

1. Typecheck de los tres servicios en un runner de GitHub.
2. Un runner **self-hosted** en el VPS hace pull de la rama, `docker compose build` y `up -d`.
3. Espera a que `django` y `postgres` estén *healthy*.
4. Aplica migraciones (`manage.py migrate`).
5. Smoke test contra `/api/health` y `/`.

En el servidor, `.systemd/orion-compose.service` levanta el stack al arrancar la máquina. El `.env`
de producción se crea a mano en el VPS y nunca viaja en git.

## Notas

- `DATABASE_URL` lleva la contraseña: solo en `.env` (ignorado por git) o en el panel del host. Nunca
  en el frontend.
- Django conecta con un rol privilegiado, así que no hay RLS de por medio: **cada endpoint de lectura
  filtra explícitamente** el contenido publicado (`activo`, `publicado`, `estado='publicado'`).
- Al cambiar modelos hay que generar la migración: el CI falla si `makemigrations --check` detecta
  cambios sin migrar.
- La carpeta `Archivos/` (ignorada por git) guarda el stack anterior en React + Supabase, documentos
  y diagramas. No se borró nada: sigue disponible en local y en el historial de git.
