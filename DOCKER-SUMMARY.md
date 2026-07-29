# Resumen de Dockerización — Orion

Este documento resume la estructura Docker agregada al proyecto.

## Archivos Creados

### 1. **Dockerfiles (servicios)**

| Archivo | Función |
|---------|---------|
| `bff-express/Dockerfile` | Build multi-stage Node.js para Express BFF |
| `backend-django/Dockerfile` | Python 3.12 + Gunicorn para Django REST |
| `frontend-vue/Dockerfile` | Build Vue 3 + Nginx para SPA |
| `nginx/Dockerfile` | Nginx Alpine para reverse proxy + TLS |

**Notas:**
- Cada Dockerfile usa `--no-cache-dir` y `--omit=dev` para minimizar tamaño
- Frontend usa multi-stage: Node para build, Nginx para runtime
- Django configura Gunicorn con 4 workers

### 2. **Configuración Nginx**

| Archivo | Función |
|---------|---------|
| `nginx/nginx.conf` | Archivo principal de configuración Nginx |
| `nginx/conf.d/default.conf` | Virtual host para HTTP/HTTPS con reverse proxy |

**Características:**
- Redirect HTTP → HTTPS
- Proxy a Frontend (`:3000`) en `/`
- Proxy a Express (`:3001`) en `/api/`
- Certificados Let's Encrypt montados como volumen read-only
- HTTP/2 sobre HTTPS

### 3. **Orquestación Docker**

| Archivo | Función |
|---------|---------|
| `docker-compose.yml` | Orquestación de 5 servicios + volúmenes + redes |

**Servicios:**
1. **nginx** — Reverse proxy, puertos 80/443
2. **frontend** — Vue SPA, puerto 3000 (interno)
3. **express** — BFF, puerto 3001 (interno)
4. **django** — API REST, puerto 8000 (interno)
5. **postgres** — Base de datos, puerto 5432 (interno)

**Características:**
- `depends_on` + `healthcheck` para startup ordenado
- Red privada `orion_net`
- Volumen `postgres_data` para persistencia
- Variables de entorno desde `.env.production`

### 4. **.dockerignore** (cada servicio)

| Archivo | Reduce tamaño excluyendo |
|---------|---------|
| `bff-express/.dockerignore` | node_modules, .env, logs, etc. |
| `backend-django/.dockerignore` | __pycache__, .venv, .env, etc. |
| `frontend-vue/.dockerignore` | node_modules, dist, .env, etc. |

### 5. **Variables de Entorno**

| Archivo | Propósito |
|---------|---------|
| `.env.production.example` | Template de `.env.production` (no commitear) |

**Variables configuradas en `.env.production`:**
- `DATABASE_URL` — Conexión PostgreSQL
- `POSTGRES_PASSWORD` — Password de BD
- `DJANGO_SECRET_KEY` — Secret Django
- `DEBUG` — Modo debug (False en prod)
- `CORS_ALLOWED_ORIGINS` — CORS whitelist
- `ALLOWED_HOSTS` — Hosts permitidos Django
- `VITE_API_URL` — URL del API para frontend
- `LETSENCRYPT_EMAIL` — Email para renovación certs

### 6. **Systemd Service**

| Archivo | Propósito |
|---------|---------|
| `.systemd/orion-compose.service` | Auto-start Docker Compose en reboot |

**Instalación:**
```bash
sudo cp .systemd/orion-compose.service /etc/systemd/system/
sudo systemctl enable orion-compose.service
sudo systemctl start orion-compose.service
```

### 7. **Documentación**

| Archivo | Contenido |
|---------|---------|
| `DEPLOYMENT.md` | Guía paso-a-paso de despliegue en Ubuntu 22.04 |
| `README.md` | (actualizado) Sección Docker agregada |
| `DOCKER-SUMMARY.md` | Este documento |

---

## Cambios en archivos existentes

### **backend-django/orion_api/urls.py**
- ✅ Agregado endpoint `/health` para Docker healthcheck

### **backend-django/orion_api/settings.py**
- ✅ Agregado `STATIC_ROOT` para `collectstatic`

### **backend-django/.env.example**
- Sin cambios (original, para desarrollo local)

### **.gitignore**
- ✅ Agregado `.env.production`, `certs/`, `backups/`, `postgres_data/`

---

## Flujo de construcción (local)

```bash
cd /opt/orion

# 1. Build imágenes (primer build: ~5-10 min)
docker compose build

# 2. Listar imágenes creadas
docker images | grep orion

# 3. Levantar servicios
docker compose up -d

# 4. Verificar salud
docker compose ps

# 5. Ver logs
docker compose logs -f django
```

**Esperado:**
- `nginx`: Up, puerto 80/443 abiertos
- `frontend`: Up
- `express`: Up, conexión Django OK
- `django`: Up (healthy), collectstatic ejecutado
- `postgres`: Up (healthy)

---

## Tamaños aproximados de imágenes

| Servicio | Base | Final |
|----------|------|-------|
| bff-express | node:20-alpine (170MB) | ~300MB |
| backend-django | python:3.12-slim (170MB) | ~700MB |
| frontend-vue | nginx:alpine (40MB) | ~100MB |
| **Total** | — | **~1.1GB** |

*Nota: Primer build descarga capas base; builds posteriores reutilizan cache.*

---

## Variables sensibles (⚠️)

Los siguientes valores NUNCA deben estar en git:
- `DATABASE_URL` (incluye password)
- `DJANGO_SECRET_KEY` (random 50+ chars)
- `POSTGRES_PASSWORD` (random 32+ chars)

**Dónde colocarlas:**
- Local (desarrollo): `.env` en cada servicio (gitignored)
- Producción: `.env.production` en raíz (gitignored) o en panel del host

---

## Testing antes de prod

```bash
# 1. Typecheck (Express + Vue)
cd bff-express && npm run typecheck
cd frontend-vue && npm run typecheck

# 2. Build local
docker compose build

# 3. Startup
docker compose up -d
sleep 30

# 4. Health checks
curl http://localhost/health        # Nginx → Frontend
curl http://localhost/api/health    # Nginx → Express → Django

# 5. Logs
docker compose logs --tail=50

# 6. Limpiar
docker compose down
```

---

## Roadmap futuro (no incluido)

- [ ] Multi-stage build para reducir tamaño de imágenes
- [ ] Private Docker registry en servidor
- [ ] Secrets management (Docker Secrets con Swarm)
- [ ] Load balancing (docker-compose scale)
- [ ] ELK/Loki para logs centralizados
- [ ] Prometheus + Grafana para métricas
- [ ] CI/CD GitHub Actions → Docker build & push
- [ ] Database migrations automáticas en startup

---

## Soporte

Errores comunes:

**Port already in use:**
```bash
sudo lsof -i :80    # Ver qué ocupa puerto 80
sudo kill -9 <PID>
```

**Imagen corrompida:**
```bash
docker compose down -v
docker system prune -a
docker compose build --no-cache
```

**Logs sin info útil:**
```bash
docker compose logs -f --timestamps
docker compose logs django --tail=100
```

---

**Última actualización:** 2026-07-29
**Rama:** `migracion-django-vue`
