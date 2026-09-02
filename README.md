# Orion Stage — Plataforma Web & Panel de Administración

Plataforma oficial de **Orion Stage Producciones SpA**, productora técnica e integral de eventos corporativos, masivos y privados en Chile.

El proyecto está diseñado con una arquitectura desacoplada y modular: SPA pública de alto impacto visual con diseño escénico *dark/luxury* y panel de administración propio (`/admin`), respaldada por una API REST en Django y PostgreSQL.

---

## 🏛 Arquitectura del Sistema

El proyecto soporta despliegue tanto en **contenedores Docker** como en **entorno nativo (cPanel / VPS con Gunicorn)**:

```
                          ┌─────────────────────────── ORION STAGE ──────────────────────────┐
                          │                                                                  │
[Navegador / Cliente] ──▶ Nginx / Apache (:80 / :443) ──┬──▶ Frontend Vue 3 (SPA Pública & Admin)
                                                        │
                                                        └──▶ API Django REST (:8000) ──▶ PostgreSQL (:5432)
                                                                    │
                                                                    ├──▶ SMTP (Notificaciones de Cotización)
                                                                    └──▶ Tablas Binarias (Imágenes WebP)
```

### Características Principales

- **Hero 3D Cover Flow:** Carrusel interactivo tridimensional en la portada que rota y escala los eventos destacados con perspectiva espacial y soporte táctil (*touch swipe*).
- **Galaxia 3D Interactiva:** Animación matemática WebGL/Canvas con inclinación espacial de 74° y rotación continua.
- **Cotizador Inteligente & Validación Dinámica:**
  - Formulario de 3 columnas con formateo automático de teléfono chileno (`+56 9 XXXX XXXX`).
  - Validación de dominios de correo y razón social.
  - Modales de campañas con visualización en alta resolución y cotización rápida integrada.
- **Notificaciones por Correo Humanizadas:**
  - Envío automático dual por SMTP: notificación detallada al productor y correo de bienvenida/confirmación cálido y cercano al cliente.
  - Integración directa con WhatsApp (`+56 9 9824 9498`) en un solo clic.
- **Panel de Administración (`/admin`):**
  - Autenticado vía Token DRF con roles de superusuario.
  - Alternador de vista: **Tarjetas (Cards)** vs **Lista (Tabla compacta)** en Servicios y Portafolio.
  - Creación y edición modal fluida (`modal-dialog-scrollable`) con subida de imágenes y galerías.
  - Enlace *"Ver sitio ↗"* con apertura en nueva pestaña (`target="_blank"`).
- **Motor de Imágenes WebP en Base de Datos:**
  - Almacenamiento binario en tabla `imagenes_archivo` sin dependencias de buckets externos.
  - Sanitización mágica de cabeceras, redimensionado a 1920 px y compresión WebP automática.
  - Servicio HTTP con encabezados inmutables y caché de 1 año (`max-age=31536000`).
- **SEO & Accesibilidad:** Metadatos Open Graph, Twitter Cards, Schema.org estructurado, `sitemap.xml` dinámico y `robots.txt` generados por Django.

---

## 🛠 Stack Tecnológico

| Capa | Tecnologías |
|---|---|
| **Frontend** | Vue 3 (Composition API, `<script setup>`), TypeScript (strict), Vite 5, Vue Router 4, Bootstrap 5, Axios, DOMPurify |
| **BFF / Proxy** | Node 20, Express, TypeScript, `http-proxy-middleware`, CORS |
| **Backend** | Python 3.12, Django 5.1, Django REST Framework, TokenAuthentication, Pillow, psycopg 3, Gunicorn |
| **Base de Datos** | PostgreSQL 16 (Local / Cloud / Contenedor) |
| **Infraestructura** | Docker Compose, Nginx, Apache / cPanel, Cloudflare SSL |

---

## 📂 Estructura del Repositorio

```
Orion_Project/
├── backend-django/          # API Django REST (App `catalogo`, modelos, endpoints y correos)
├── bff-express/             # Proxy fino Express + TypeScript
├── frontend-vue/            # SPA Vue 3 + TypeScript (Vistas públicas + /admin)
├── nginx/                   # Configuración del reverse proxy Nginx
├── Archivos/                # [IGNORADO EN GIT] Material histórico, guías PDF, diagramas y capturas
│   ├── 01_Guias_y_Manuales_PDF/
│   ├── 02_Diagramas_HTML/
│   ├── 03_Campanas_Publicitarias/
│   ├── 04_Cotizaciones_y_Comprobantes/
│   ├── 05_Identidad_Visual_y_Textos/
│   ├── 06_Credenciales_y_Capturas/
│   ├── 07_Incidencias_Tecnicas/
│   └── 08_Stack_Anterior_React_Supabase/
├── docker-compose.yml       # Stack completo para producción/staging
├── docker-compose.preprod.yml
├── .env.production.example  # Plantilla de variables de entorno
├── AGENTS.md                # Reglas y directivas de desarrollo
└── README.md                # Documentación del proyecto
```

---

## 🚀 Despliegue y Ejecución

### 1. Despliegue con Docker Compose

```bash
# Copiar variables de entorno y configurar credenciales
cp .env.production.example .env

# Levantar todos los servicios en segundo plano
docker compose up -d --build
```

El sitio estará disponible en `http://localhost`. Para monitorear logs:
```bash
docker compose logs -f
```

### 2. Desarrollo Local Servicio por Servicio

```bash
# Backend Django
cd backend-django
python -m venv .venv
# En Windows: .venv\Scripts\activate | En Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

# BFF Express
cd bff-express
npm install
npm run dev

# Frontend Vue
cd frontend-vue
npm install
npm run dev
```

---

## 🔐 Panel de Administración y Superusuarios

El acceso al panel administrativo se realiza desde la ruta `/admin/login` en la SPA.

* **Crear Superusuario:**
  ```bash
  cd backend-django
  python manage.py createsuperuser
  ```

---

## 🧪 Verificación de Calidad y Puertas de CI

Antes de subir cambios a `main`, ejecuta las verificaciones obligatorias:

```bash
# 1. Compilación y chequeo de tipos en Frontend
cd frontend-vue && npm run build

# 2. Chequeo de tipos en BFF
cd bff-express && npm run typecheck

# 3. Integridad del Backend Django y migraciones
cd backend-django && python manage.py check
cd backend-django && python manage.py makemigrations --check --dry-run
```

---

## 📄 Convenciones del Proyecto

* **Idioma del Dominio:** Español para modelos, rutas, funciones y variables de negocio (`servicios`, `eventos`, `cotizaciones`, `portafolio/:slug`).
* **Estilos:** Bootstrap 5 con variables personalizadas CSS (`--orion-*`) con soporte integral de tema claro y oscuro.
* **Archivos y Documentación:** Todos los manuales PDF, comprobantes, contratos y material histórico se almacenan localmente en `Archivos/` y permanecen estrictamente fuera del repositorio git (`.gitignore`).

