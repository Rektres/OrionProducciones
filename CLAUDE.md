# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Sitio web de **Orion**, productora de eventos (Chile). SPA en React + TypeScript + Vite, con Supabase como backend (Postgres + RLS). Sitio de solo lectura para el público: consume contenido (servicios, portafolio, blog) y permite crear cotizaciones. No hay panel de admin ni autenticación; el contenido se edita directamente en Supabase.

Idioma del dominio: **español** — tablas, campos, tipos y slugs de rutas están en español (`servicios`, `eventos`, `cotizaciones`, `portafolio/:slug`). Mantén esa convención al agregar código.

## Comandos

```bash
npm run dev        # servidor de desarrollo (http://localhost:5173)
npm run build      # build de producción a dist/
npm run preview    # sirve el build
npm run lint       # ESLint sobre todo el repo
npm run typecheck  # tsc --noEmit -p tsconfig.app.json (no hay tests)
```

No hay suite de tests. Antes de declarar un cambio listo, corre `npm run typecheck` y `npm run lint`.

## Variables de entorno

Requeridas en `.env` (raíz). `src/lib/supabase.ts` lanza error en runtime si faltan las dos primeras:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_WHATSAPP_NUMBER` (número del botón flotante de WhatsApp)

## Arquitectura

**Flujo de datos:** páginas (`src/pages/`) → servicios (`src/services/`) → cliente Supabase (`src/lib/supabase.ts`). Las páginas nunca hablan con Supabase directamente; siempre pasan por un service. Cada service exporta un objeto con métodos async (`servicioService`, `blogService`, `portafolioService`, `contactoService`) que devuelven tipos de `src/types/index.ts` y hacen `throw error` en fallo.

**Patrón de query:** los services filtran por el flag de publicación en el cliente (`.eq('activo', true)`, `.eq('estado', 'publicado')`, `.eq('publicado', true)`), pero **RLS en Supabase ya restringe** las filas visibles al rol `anon` a solo contenido publicado. Al agregar tablas/queries, replica ambas capas: policy de RLS pública para lectura + filtro en el service.

**Rutas** (`src/App.tsx`, React Router v7): `/`, `/servicios`, `/portafolio`, `/portafolio/:slug`, `/blog`, `/blog/:slug`.

**Componentes** (`src/components/`):
- `ui/` — primitivos reutilizables (Button, Card, Modal, Badge), exportados vía `index.ts`
- `layout/` — Navbar, Footer, WhatsAppButton
- `animations/` — FadeInUp, StaggerContainer, ParticleBackground (Framer Motion)
- `shared/` — ContactForm (crea cotizaciones)

**Alias de import:** `@/` → `src/` (configurado en `vite.config.ts`). Usa `@/services/...`, `@/types`, etc.

**Base de datos:** migraciones en `supabase/migrations/` (`001_create_initial_schema.sql` define tablas + RLS + índices; `002_seed_initial_data.sql` carga datos de ejemplo). Todas las tablas tienen RLS habilitado. `cotizaciones` es la única tabla con INSERT público; el resto es solo SELECT para publicados. Al cambiar el esquema, agrega una nueva migración — no edites las existentes.

## Convenciones

- TypeScript en modo `strict` con `noUnusedLocals`/`noUnusedParameters` — no dejes imports ni parámetros sin usar o el typecheck falla.
- Iconos: solo `lucide-react`. No agregar librerías de UI/iconos (ver `.bolt/prompt`).
- Estilos: Tailwind. Paleta custom en `tailwind.config.js` (`primary` coral, `secondary` amarillo, `tertiary` violeta).
- Contenido HTML del blog se sanitiza con DOMPurify antes de renderizar.
- Accesibilidad: respeta `prefers-reduced-motion` vía el hook `useReducedMotion` al agregar animaciones.

## Notas

- La Edge Function `send-cotizacion-email` que invoca `contactoService.notificarAdminCotizacion` **no está en el repo** (solo documentada en `SETUP.md`); su fallo se traga con `console.error` y no rompe el envío de la cotización.
- Deploy pensado para Vercel/Netlify (SPA estática); las variables `VITE_*` se configuran en el dashboard del host.
