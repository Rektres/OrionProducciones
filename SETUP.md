# Orion - Productora de Eventos

Página web moderna y responsiva para productora de eventos con backend Supabase.

## Inicio Rápido

### 1. Configurar Variables de Entorno

Edita el archivo `.env` en la raíz del proyecto:

```env
VITE_SUPABASE_URL=tu_supabase_url
VITE_SUPABASE_ANON_KEY=tu_supabase_anon_key
VITE_WHATSAPP_NUMBER=56944830378
```

Obtén estas variables:
1. Ve a [Supabase](https://supabase.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a Settings → API
4. Copia `Project URL` y `anon public key`

### 2. Base de Datos

La base de datos ya está configurada con todas las tablas necesarias:

- `categorias_servicio` - Categorías de servicios
- `servicios` - Servicios ofrecidos
- `evento_tipos` - Tipos de eventos
- `eventos` - Eventos del portafolio
- `fotos_evento` - Galería de fotos
- `tags` - Etiquetas del blog
- `posts` - Artículos del blog
- `post_tags` - Relación posts-tags
- `cotizaciones` - Solicitudes de cotización

Todos los datos iniciales están pre-cargados.

### 3. Estructura del Proyecto

```
src/
├── components/
│   ├── animations/       # ParticleBackground, FadeInUp, StaggerContainer
│   ├── layout/          # Navbar, Footer, WhatsAppButton
│   ├── ui/              # Button, Card, Modal, Badge
│   └── shared/          # ContactForm, etc
├── pages/
│   ├── Landing.tsx
│   ├── Servicios.tsx
│   ├── Portafolio.tsx
│   └── Blog.tsx
├── services/
│   ├── servicios.service.ts
│   ├── portafolio.service.ts
│   ├── blog.service.ts
│   └── contacto.service.ts
├── hooks/
│   └── useReducedMotion.ts
├── types/
│   └── index.ts
├── lib/
│   └── supabase.ts
└── App.tsx
```

### 4. Rutas Disponibles

- `/` - Landing page (inicio)
- `/servicios` - Página de servicios con filtros
- `/portafolio` - Galería de eventos
- `/portafolio/:slug` - Detalle de evento
- `/blog` - Blog con paginación
- `/blog/:slug` - Artículo completo

### 5. Características Implementadas

✅ **Frontend:**
- Diseño responsive con Tailwind CSS
- Animaciones suaves con Framer Motion
- Paleta de colores personalizada (Coral, Amarillo, Violeta)
- Tipografía premium (Bebas Neue, Space Grotesk, Inter)
- Efectos visuales (Partículas animadas, glassmorphism)
- Botón WhatsApp flotante
- Formulario de contacto con validación

✅ **Backend:**
- Base de datos Supabase configurada
- Row Level Security (RLS) habilitado
- Servicios de lectura para contenido público
- Servicio de contacto para cotizaciones

✅ **Componentes:**
- 4 páginas principales (Landing, Servicios, Portafolio, Blog)
- Sistema de componentes reutilizables
- Animaciones de entrada escalonadas
- Lightbox para galería de fotos
- Grid masonry responsivo

### 6. Próximos Pasos Opcionales

1. **Edge Functions para emails:**
   ```bash
   # Crear función para enviar emails de cotización
   supabase functions new send-cotizacion-email
   ```

2. **Hosting:**
   - Vercel (recomendado para React)
   - Netlify
   - AWS S3 + CloudFront

3. **Personalización:**
   - Cambiar colores en `tailwind.config.js`
   - Actualizar datos en Supabase
   - Agregar redes sociales en Footer

4. **Dominio:**
   - Apuntar DNS a tu hosting
   - Configurar SSL/TLS

### 7. Tecnologías Utilizadas

- **React 18** - Framework principal
- **TypeScript** - Type safety
- **Vite** - Bundler
- **Tailwind CSS** - Estilos
- **Framer Motion** - Animaciones
- **Supabase** - Backend y Base de datos
- **React Router** - Navegación
- **Lucide React** - Iconos
- **DOMPurify** - Sanitización HTML

### 8. Tips de Desarrollo

- Usa `npm run dev` para desarrollo local
- `npm run build` para compilar para producción
- `npm run lint` para verificar código
- Los tipos TypeScript están en `src/types/index.ts`
- Los servicios de API están en `src/services/`

### 9. Datos Iniciales

El proyecto viene con datos de ejemplo:

- 6 servicios (Corporativos y Sociales)
- 4 eventos en el portafolio
- 3 artículos en el blog
- Etiquetas de blog

Todos estos pueden editarse directamente en Supabase.

## Licencia

Desarrollado por Mateo Araneda Medina
