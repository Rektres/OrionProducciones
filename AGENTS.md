# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Proyecto

Sitio web de **Orion**, productora de eventos (Chile). Stack de cuatro servicios en Docker: SPA Vue 3 →
BFF Express → API Django REST → PostgreSQL, todo detrás de un Nginx que es el único puerto expuesto.
El sitio público es de solo lectura (servicios, portafolio, FAQ) y permite crear cotizaciones; el
contenido se administra desde `/admin`, un panel propio dentro de la misma SPA autenticado con token DRF.

Idioma del dominio: **español** — tablas, campos, tipos, slugs de rutas y nombres de funciones nuevas
van en español (`servicios`, `eventos`, `cotizaciones`, `portafolio/:slug`). Mantén esa convención.

## Estructura

```
frontend-vue/    Vue 3 + TS + Vite + Bootstrap 5. SPA pública + panel /admin.
bff-express/     Express + TS. Proxy fino: reenvía /api/* a Django (CORS, streaming de multipart).
backend-django/  Django 5 + DRF. App única `catalogo`: modelos, endpoints públicos y admin.
nginx/           Reverse proxy. "/" → frontend, "/api/" → BFF, "/robots.txt" y "/sitemap.xml" → Django.
Archivos/        Material archivado (stack React+Supabase anterior, docs, diagramas). Ignorado por git.
```

## Comandos

```bash
docker compose up -d --build     # stack completo en http://localhost

cd frontend-vue && npm run dev        # SPA en http://localhost:5173
cd frontend-vue && npm run typecheck  # vue-tsc --noEmit
cd frontend-vue && npm run build      # typecheck + build a dist/

cd bff-express && npm run typecheck

cd backend-django && python manage.py check
cd backend-django && python manage.py makemigrations --check --dry-run
```

No hay suite de tests. Antes de declarar un cambio listo corre, según lo que tocaste,
`npm run build` en `frontend-vue/` y `manage.py check` + `makemigrations --check` en `backend-django/`.
Son las mismas puertas que corre el CI.

## Variables de entorno

`.env` en la raíz alimenta a docker-compose (`DATABASE_URL`, `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`,
`ALLOWED_ORIGINS`, `SERVER_IP`, credenciales SMTP). El frontend usa su propio `.env`; ver
`frontend-vue/.env.example` para la lista completa (API, WhatsApp, redes, contacto, analítica).

## Arquitectura

**Flujo de datos:** vistas (`frontend-vue/src/views/`) → servicios (`src/services/`) → `api.ts` (axios) →
Nginx → BFF → Django. Las vistas nunca llaman a axios directamente; siempre pasan por un service.

**Autenticación:** solo el panel. `/api/auth/token/` devuelve un token DRF que `adminAuth` guarda en
localStorage; el interceptor de `api.ts` lo adjunta y desloguea ante un 401. Los endpoints admin usan
`TokenAuthentication` + `IsAuthenticated`; el resto es lectura pública de contenido publicado.

**Imágenes:** se guardan como binario en la tabla `imagenes_archivo` (no hay storage externo).
`catalogo/imagenes.py` valida tamaño, MIME y firma mágica, y recodifica a WebP reescalando a 1920 px.
Se sirven por `/api/imagenes/<uuid>/` con cache inmutable.

**SEO:** `frontend-vue/src/composables/useSeo.ts` escribe title, description, canonical y Open Graph por
ruta (metadatos en `router/index.ts`). Los crawlers que no ejecutan JS leen las etiquetas estáticas de
`index.html`. `robots.txt` y `sitemap.xml` los genera Django en `catalogo/seo.py`.

**Base de datos:** migraciones de Django en `backend-django/catalogo/migrations/`. Al cambiar modelos,
genera la migración — el CI falla si `makemigrations --check` detecta cambios sin migrar.

## Convenciones

- TypeScript en modo `strict` con `noUnusedLocals`/`noUnusedParameters`: no dejes imports ni parámetros sin usar.
- Iconos y UI: Bootstrap 5 y SVG inline. No agregar librerías de UI ni de iconos.
- Estilos: clases de Bootstrap + variables CSS propias en `frontend-vue/src/style.css` (`--orion-*`).
  Hay tema claro y oscuro: cualquier color nuevo debe funcionar en ambos.
- HTML de contenido (FAQ) se sanitiza con DOMPurify antes de renderizar.
- Imágenes públicas van en `<img>` con `alt` descriptivo y `loading="lazy"` (clase `.img-cover`),
  nunca como `background-image`: así quedan accesibles e indexables.

## Despliegue

Push a `main` o a `migracion-django-vue` dispara `.github/workflows/deploy-docker.yml`: typecheck de los tres
servicios, luego un runner self-hosted en el VPS hace pull, `docker compose build`, espera healthchecks,
aplica migraciones y corre un smoke test. Detalle en `DEPLOYMENT.md` (local, fuera del repo).
