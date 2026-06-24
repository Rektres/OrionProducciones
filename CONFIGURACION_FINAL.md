# Configuración Final - Productora Orion

## Paso 1: Configurar Supabase

### 1.1 Crear Proyecto en Supabase
1. Ve a https://supabase.com
2. Crea una cuenta (si no tienes)
3. Crea un nuevo proyecto
4. Espera a que se inicialice (2-3 minutos)

### 1.2 Obtener Credenciales
1. En tu proyecto, ve a **Settings** → **API**
2. Copia el **Project URL** (ej: `https://xxxxx.supabase.co`)
3. Copia el **anon public key** (la larga que empieza con `eyJhbG...`)

### 1.3 Configurar .env
Edita `/tmp/cc-agent/66786490/project/.env`:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbG...
VITE_WHATSAPP_NUMBER=56944830378
```

## Paso 2: Verificar Base de Datos

Las tablas se crearon automáticamente con los datos iniciales:

1. En Supabase, ve a **Table Editor**
2. Deberías ver:
   - `categorias_servicio` (4 registros)
   - `servicios` (6 registros)
   - `evento_tipos` (4 registros)
   - `eventos` (4 registros)
   - `tags` (6 registros)
   - `posts` (3 registros)
   - `cotizaciones` (vacía, se llena con formularios)

Si algo falta, las migraciones están en **SQL Editor** → **Check migrations**

## Paso 3: Publicar en Internet

### Opción A: Vercel (Recomendado)
```bash
# 1. Instala Vercel CLI
npm install -g vercel

# 2. Desde la carpeta del proyecto
vercel

# 3. Sigue las instrucciones
# 4. Configura variables de entorno en Vercel Dashboard
```

### Opción B: Netlify
```bash
# 1. Haz push a GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin tu-repo-github
git push -u origin main

# 2. Ve a netlify.com
# 3. Conecta tu repositorio GitHub
# 4. Configura build: npm run build
# 5. Configura variables de entorno
```

### Opción C: AWS S3 + CloudFront
1. Compila: `npm run build`
2. Sube la carpeta `dist/` a S3
3. Configura CloudFront para servir desde S3
4. Apunta tu dominio a CloudFront

## Paso 4: Configurar Dominio

Si compraste un dominio (godaddy, namecheap, etc):

1. Obtén los **nameservers** de tu proveedor de hosting
2. En tu registrador de dominio, apunta los nameservers
3. Espera 24-48 horas para propagación

## Paso 5: Edge Functions para Emails (Opcional)

Crear una función para enviar emails cuando alguien cotiza:

```bash
# En la carpeta del proyecto
supabase functions new send-cotizacion-email
```

Contenido de `supabase/functions/send-cotizacion-email/index.ts`:

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Info, Apikey',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const { cotizacionId } = await req.json();

    // Aquí iría el código para enviar email
    // Usando SendGrid, Resend, o similar

    return new Response(
      JSON.stringify({ success: true }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
```

Luego:
```bash
supabase functions deploy send-cotizacion-email
```

## Paso 6: Personalizar Contenido

### Cambiar Datos en Supabase

En **Table Editor**, edita directamente:

- **servicios**: Añade/edita servicios
- **eventos**: Añade eventos del portafolio
- **posts**: Escribe artículos de blog
- **tags**: Crea categorías para posts

### Cambiar Colores

En `tailwind.config.js`:
```js
colors: {
  primary:    '#FF3D6B',  // Coral
  secondary:  '#FFB800',  // Amarillo
  tertiary:   '#6B2FFA',  // Violeta
  // ... más colores
}
```

### Cambiar Números (Landing Stats)

En `src/pages/Landing.tsx`, busca la sección "Stats Section" y modifica:
```tsx
{ number: '+150', label: 'Eventos realizados' }
```

## Paso 7: Agregar Redes Sociales

En `src/components/layout/Footer.tsx`:
```tsx
<a href="https://instagram.com/tuinstagram" className="hover:text-primary">
  Instagram
</a>
```

## Verificación Final

```bash
# Compilar y verificar
npm run build

# Ejecutar localmente
npm run dev

# Abrir en navegador
# http://localhost:5173
```

Verifica:
- [ ] Landing carga correctamente
- [ ] Servicios aparecen
- [ ] Portafolio carga eventos
- [ ] Blog muestra posts
- [ ] Formulario de contacto funciona
- [ ] WhatsApp button funciona
- [ ] Navbar es responsivo
- [ ] Animaciones funcionan suave
- [ ] Colores se ven correctos

## Soporte

- **Documentación Supabase**: https://supabase.com/docs
- **React Router**: https://reactrouter.com/en/main
- **Framer Motion**: https://www.framer.com/motion/
- **Tailwind CSS**: https://tailwindcss.com/docs

## Notas Importantes

- El proyecto respeta `prefers-reduced-motion` (accesibilidad)
- Todas las tablas tienen RLS habilitado
- TypeScript está en modo strict
- Build está optimizado (~150KB gzip)
- Las imágenes usan URLs de Pexels (stock photos)

## Contacto

Desarrollado por Mateo Araneda Medina
