# Orion — Productora de Eventos

Sitio web de **Orion**, productora de eventos (Chile). SPA en React + TypeScript + Vite que consume contenido desde Supabase (servicios, portafolio, blog) y permite enviar cotizaciones. Incluye un API opcional en Node/Express.

## Stack

- **React 18** + **TypeScript** + **Vite**
- **Tailwind CSS** (tema oscuro, paleta custom) + **Framer Motion** (animaciones)
- **Supabase** (Postgres + RLS) como backend
- **React Router v7**, **Lucide** (iconos), **DOMPurify** (sanitización de HTML del blog)
- API opcional: **Express** + TypeScript (`tsx`)

## Requisitos

- **Node.js 18+** y npm.
  > En este equipo Node está en `C:\Users\mateo.araneda\node` (ya agregado al PATH de usuario). Si `npm` no se reconoce en una terminal nueva, ciérrala y abre otra, o usa la ruta completa `C:\Users\mateo.araneda\node\npm`.
- Un proyecto **Supabase** con sus credenciales (Project URL + anon/publishable key; service_role solo si usas el API).

## Estructura

```
.
├── src/                      # Frontend (React)
│   ├── components/           # ui/ (Button, Card, Modal, Badge), layout/, animations/, shared/
│   ├── pages/                # Landing, Servicios, Portafolio, Blog
│   ├── services/             # Acceso a Supabase (servicios, portafolio, blog, contacto)
│   ├── lib/supabase.ts       # Cliente Supabase del frontend
│   └── types/                # Tipos TypeScript
├── server/                   # API Node/Express (opcional)
│   ├── src/routes/           # servicios, portafolio, blog, cotizaciones
│   └── src/supabase.ts       # Cliente Supabase del API (service_role)
├── supabase/migrations/      # Esquema + datos iniciales (SQL)
└── index.html
```

## Configuración de variables de entorno

### Frontend — `.env` en la raíz

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=tu_anon_o_publishable_key
VITE_WHATSAPP_NUMBER=56944830378
```

Las credenciales se obtienen en Supabase → **Settings → API** (`Project URL` y `anon public key`). El frontend **no arranca** si faltan `VITE_SUPABASE_URL` o `VITE_SUPABASE_ANON_KEY`.

### API (opcional) — `server/.env`

Copia `server/.env.example` y complétalo:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key
PORT=3001
ALLOWED_ORIGINS=http://localhost:5173
```

> La `service_role` key **nunca** debe exponerse al cliente ni ir en variables `VITE_*`. Ambos `.env` están en `.gitignore`.

## Correr en local

### Frontend

```bash
npm install
npm run dev          # http://localhost:5173
```

### API (opcional, en otra terminal)

```bash
cd server
npm install
npm run dev          # http://localhost:3001
```

Abre **http://localhost:5173** en el navegador. El sitio funciona solo con el frontend (habla directo a Supabase); el API es aditivo.

## Scripts

### Frontend (raíz)

| Comando | Descripción |
|---|---|
| `npm run dev` | Servidor de desarrollo (Vite) |
| `npm run build` | Build de producción a `dist/` |
| `npm run preview` | Sirve el build |
| `npm run lint` | ESLint |
| `npm run typecheck` | Chequeo de tipos (`tsc`) |

### API (`server/`)

| Comando | Descripción |
|---|---|
| `npm run dev` | API en watch mode |
| `npm start` | Levanta el API |
| `npm run typecheck` | Chequeo de tipos |

## Rutas del sitio

- `/` — Landing
- `/servicios` — Servicios con filtros
- `/portafolio` y `/portafolio/:slug` — Portafolio y detalle
- `/blog` y `/blog/:slug` — Blog y artículo

## Endpoints del API

- `GET /health`
- `GET /api/servicios/categorias`, `GET /api/servicios?categoria=<slug>`, `GET /api/servicios/:id`
- `GET /api/portafolio/tipos`, `GET /api/portafolio/eventos?tipo=&destacado=`, `GET /api/portafolio/eventos/:slug`, `GET /api/portafolio/eventos/:id/fotos`
- `GET /api/blog/posts?limit=&offset=&tag=`, `GET /api/blog/posts/:slug`, `GET /api/blog/tags`
- `POST /api/cotizaciones`

## Base de datos

El esquema y los datos iniciales están en `supabase/migrations/`. Todas las tablas tienen **RLS** habilitado: lectura pública solo de contenido publicado, e inserción pública únicamente en `cotizaciones`. Para cambiar el esquema, agrega una **nueva migración** (no edites las existentes).

## Deploy

Build estático (`npm run build`) desplegable en Vercel o Netlify. Configura las variables `VITE_*` en el dashboard del host.

## Notas

- El proyecto respeta `prefers-reduced-motion` (accesibilidad).
- ⚠️ Si trabajas dentro de OneDrive y falla con *"Failed to load /src/main.tsx"*, corre `git restore src` (OneDrive puede mover/eliminar archivos). Se recomienda mover el proyecto fuera de OneDrive.

---

Desarrollado por Mateo Araneda Medina.
