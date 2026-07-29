# Dockerización y Despliegue en Servidor Linux — Orion

## Overview

Este documento guía la dockerización completa del proyecto Orion (Vue 3 SPA + Express BFF + Django REST + PostgreSQL) para despliegue en un servidor Ubuntu 22.04 LTS.

**Arquitectura:**
```
[ Nginx (reverse proxy, TLS) ]
    ↓           ↓
[ Vue SPA ]  [ Express BFF ]
               ↓
           [ Django REST ]
               ↓
           [ PostgreSQL ]
```

---

## Pre-requisitos

✅ Los siguientes archivos ya están en el repo:
- `Dockerfile` en cada servicio (bff-express, backend-django, frontend-vue)
- `nginx/Dockerfile`, `nginx/nginx.conf`, `nginx/conf.d/default.conf`
- `docker-compose.yml` en raíz
- `.dockerignore` en cada servicio
- `.env.production.example` como template
- `.systemd/orion-compose.service` para auto-start

---

## Despliegue en Ubuntu 22.04 LTS

### **Paso 1: Preparar servidor**

```bash
# SSH al servidor
ssh user@server.example.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker & Docker Compose
sudo apt install -y docker.io docker-compose-plugin curl git

# Add user 'orion' to docker group (opcional, evita sudo en cada comando)
sudo useradd -m -s /bin/bash orion
sudo usermod -aG docker orion

# Clone repository
sudo mkdir -p /opt/orion
sudo git clone https://github.com/Rektres/Orion_Project.git /opt/orion
cd /opt/orion
git checkout migracion-django-vue
sudo chown -R orion:orion /opt/orion
```

### **Paso 2: Crear `.env.production` con secrets**

```bash
cd /opt/orion

# Generar valores aleatorios seguros
POSTGRES_PW=$(openssl rand -base64 32)
DJANGO_SECRET=$(openssl rand -base64 50)

cat > .env.production <<EOF
# DATABASE
DATABASE_URL=postgresql://postgres:${POSTGRES_PW}@postgres:5432/orion
POSTGRES_PASSWORD=${POSTGRES_PW}

# DJANGO
DJANGO_SECRET_KEY=${DJANGO_SECRET}
DEBUG=False

# HOSTS / CORS (⚠️ reemplazar con dominio real)
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
ALLOWED_HOSTS=example.com,www.example.com

# BFF / FRONTEND
VITE_API_URL=https://example.com/api
VITE_WHATSAPP_NUMBER=56944830378
VITE_BASE=/

# NGINX / LETSENCRYPT
LETSENCRYPT_EMAIL=admin@example.com
EOF

chmod 600 .env.production
```

**⚠️ Reemplazar:**
- `example.com` → tu dominio real
- `admin@example.com` → tu email real
- `56944830378` → número WhatsApp si corresponde

### **Paso 3: Obtener certificado SSL con Let's Encrypt**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado (requiere puerto 80 abierto)
sudo certbot certonly --standalone \
  -d example.com \
  -d www.example.com \
  --agree-tos \
  -m admin@example.com \
  --non-interactive

# Copiar certs al proyecto
sudo mkdir -p /opt/orion/certs
sudo cp -r /etc/letsencrypt/live /opt/orion/certs/
sudo chown -R orion:orion /opt/orion/certs
```

Verifica:
```bash
ls -la /opt/orion/certs/live/example.com/
# Debe mostrar: fullchain.pem, privkey.pem
```

### **Paso 4: Build Docker images**

```bash
cd /opt/orion

# Build imágenes (toma 5-10 min según conexión)
docker compose build

# Verifica que se cargó .env.production
docker compose config | grep "DATABASE_URL"
```

### **Paso 5: Crear volumen de BD e inicializar**

```bash
# Crear carpeta de backups
mkdir -p /opt/orion/backups

# Start servicios (Django es el último para que migre la BD)
docker compose up -d

# Esperar ~30s para que todos levanten
sleep 30

# Verificar estado
docker compose ps
```

**Esperado:**
```
NAME         STATUS
nginx        Up (healthy)
frontend     Up
express      Up
django       Up (healthy)
postgres     Up (healthy)
```

### **Paso 6: Registrar como systemd service (auto-start)**

```bash
# Crear directorio systemd
sudo mkdir -p /etc/systemd/system

# Copiar archivo de servicio
sudo cp /opt/orion/.systemd/orion-compose.service /etc/systemd/system/

# Editar si es necesario (verificar WorkingDirectory y User)
sudo nano /etc/systemd/system/orion-compose.service

# Recargar daemon
sudo systemctl daemon-reload

# Habilitar y arrancar
sudo systemctl enable orion-compose.service
sudo systemctl start orion-compose.service

# Verificar estado
sudo systemctl status orion-compose.service
```

### **Paso 7: Verificación final**

```bash
# Todos los servicios corriendo
docker compose ps

# Puertos abiertos
sudo netstat -tuln | grep -E '80|443'

# Test HTTP→HTTPS redirect
curl -i http://example.com
# Debe devolver: 301 (redirect a HTTPS)

# Test HTTPS
curl -i https://example.com
# Debe devolver: 200 OK (desde Nginx)

# Test API (a través de Express)
curl -i https://example.com/api/servicios
# Debe devolver: JSON desde Django

# Ver logs completos
docker compose logs --tail=50

# Logs específicos
docker compose logs django
docker compose logs express
docker compose logs nginx
```

---

## Operaciones comunes

### **Ver logs en tiempo real**

```bash
docker compose logs -f
docker compose logs -f django
docker compose logs -f express
```

### **Ejecutar migraciones de Django**

```bash
docker compose exec django python manage.py migrate
```

### **Backup de base de datos**

```bash
docker compose exec postgres pg_dump -U postgres orion > /opt/orion/backups/orion_$(date +%Y%m%d).sql
```

### **Restaurar base de datos**

```bash
docker compose exec -T postgres psql -U postgres -d orion < /opt/orion/backups/orion_20240101.sql
```

### **Reiniciar servicio específico**

```bash
docker compose restart django
docker compose restart express
docker compose restart frontend
```

### **Detener e iniciar todo**

```bash
# Detener
docker compose down

# Iniciar
docker compose up -d
```

### **Ver variables de entorno cargadas**

```bash
docker compose exec django env | grep -E "DATABASE|DJANGO_SECRET|DEBUG|CORS"
```

---

## Renovación de certificados SSL (automático)

Certbot renueva automáticamente 30 días antes de expiración:

```bash
# Verificar renovación seca (sin hacer cambios)
sudo certbot renew --dry-run

# Forzar renovación
sudo certbot renew --force-renewal

# Ver próxima renovación
sudo certbot certificates
```

---

## Troubleshooting

### **Django no conecta a PostgreSQL**

```bash
# Verificar .env.production
cat /opt/orion/.env.production | grep DATABASE_URL

# Check logs
docker compose logs django | tail -20

# Verificar conectividad desde Express hacia Django
docker compose exec express curl -v http://django:8000/health
```

### **Nginx devuelve 502 Bad Gateway**

```bash
# Express no está respondiendo
docker compose logs express

# Verificar puerto
docker compose exec express lsof -i :3001
```

### **Certificado SSL expirado**

```bash
# Renovar manualmente
sudo certbot renew --force-renewal

# Copiar nuevos certificados
sudo cp -r /etc/letsencrypt/live /opt/orion/certs/
sudo chown -R orion:orion /opt/orion/certs

# Reiniciar Nginx
docker compose restart nginx
```

### **Puertos ya en uso**

```bash
# Verificar qué proceso usa puerto 80/443
sudo lsof -i :80
sudo lsof -i :443

# Matar proceso
sudo kill -9 <PID>

# O cambiar puerto en docker-compose.yml
```

---

## Seguridad (Checklist)

- [ ] `.env.production` no está en git (gitignored)
- [ ] `DEBUG=False` en producción
- [ ] `DJANGO_SECRET_KEY` es aleatorio y largo (50+ caracteres)
- [ ] Firewall permite solo 80/443 (no 3001, 8000, 5432)
- [ ] Backups de BD hechos regularmente
- [ ] SSL/TLS vigente (chequear `certbot certificates`)
- [ ] CORS_ALLOWED_ORIGINS no incluye wildcard `*`
- [ ] Base de datos PostgreSQL no expuesta (solo acceso interno)

---

## Monitoreo recomendado

```bash
# Health check manual (cada 5 min via cron)
docker compose exec django curl -s http://localhost:8000/health || notify-admin

# Logs centralizados (opcional)
# Considerar ELK stack (Elasticsearch/Logstash/Kibana) o Loki

# Métricas (opcional)
# Prometheus + Grafana para CPU/RAM/Disco de contenedores
```

---

## Rollback a versión anterior

```bash
cd /opt/orion

# Ver último commit conocido bueno
git log --oneline | head -5

# Revertir
git checkout <commit-hash>

# Rebuild y restart
docker compose down
docker compose build
docker compose up -d
```

---

## Guía de URLs post-despliegue

- **Frontend (SPA):** `https://example.com`
- **API Gateway:** `https://example.com/api/*`
- **Health check:** `https://example.com/api/health` (desde Express)
- **Django directo:** Accesible solo internamente en `http://django:8000/api/*`

---

## Contacto & Soporte

Para issues con Docker/Compose:
```bash
docker --version
docker compose version
```

Ver logs detallados:
```bash
docker compose logs --follow --timestamps
```
