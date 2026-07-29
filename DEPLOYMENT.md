# Despliegue en Ubuntu Server — Orion

Guía para levantar el stack completo (Nginx + Vue + Express + Django + PostgreSQL) en tu
servidor Ubuntu, accediendo por **IP pública** (sin dominio ni SSL por ahora).

Todo el stack corre en contenedores propios — el `docker-compose.yml` incluye su propio
PostgreSQL, no depende de Supabase.

---

## 0. Requisitos previos

- Servidor Ubuntu Server (20.04+) con acceso SSH y usuario con permisos `sudo`.
- IP pública del servidor (ej. `203.0.113.10`) — la necesitarás en el paso 3.
- Docker ya instalado (según mencionaste). Verifica:

```bash
docker --version
docker compose version
```

Si falta alguno, instálalo:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER   # evita usar sudo en cada comando docker
newgrp docker                    # aplica el grupo sin cerrar sesión
```

---

## 1. Clonar el repositorio

```bash
sudo mkdir -p /opt/orion
sudo chown $USER:$USER /opt/orion
git clone https://github.com/Rektres/Orion_Project.git /opt/orion
cd /opt/orion
git checkout migracion-django-vue
```

---

## 2. Abrir puertos en el firewall

Solo necesitas **80** (HTTP) abierto al público. El resto de servicios (Express, Django,
Postgres) quedan solo en la red interna de Docker — nunca expuestos al exterior.

```bash
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status
```

Si tu proveedor cloud (AWS/GCP/Azure/DigitalOcean) tiene su propio firewall/security group,
abre el puerto **80** ahí también.

---

## 3. Crear `.env.production` con tus valores reales

```bash
cd /opt/orion
cp .env.production.example .env.production
```

Genera secrets seguros y edita el archivo:

```bash
# Generar valores aleatorios
openssl rand -base64 32   # usar para POSTGRES_PASSWORD
openssl rand -base64 50   # usar para DJANGO_SECRET_KEY
```

Edita `.env.production`:

```bash
nano .env.production
```

Contenido esperado (reemplaza `TU_IP_PUBLICA` por la IP real del servidor, y las
contraseñas por las generadas arriba):

```bash
DATABASE_URL=postgresql://postgres:TU_PASSWORD_GENERADO@postgres:5432/orion
POSTGRES_PASSWORD=TU_PASSWORD_GENERADO

DJANGO_SECRET_KEY=TU_SECRET_KEY_GENERADO
DEBUG=False
DB_SSL_REQUIRE=False

SERVER_IP=TU_IP_PUBLICA
ALLOWED_ORIGINS=http://TU_IP_PUBLICA
```

⚠️ `POSTGRES_PASSWORD` debe coincidir con el password dentro de `DATABASE_URL`.

```bash
chmod 600 .env.production
```

**Vincula este archivo como el `.env` que usará docker compose:**

```bash
ln -sf .env.production .env
```

---

## 4. Build de las imágenes

```bash
cd /opt/orion
docker compose build
```

Esto toma ~5-10 min la primera vez (descarga imágenes base + instala dependencias).

---

## 5. Levantar el stack

```bash
docker compose up -d
```

Espera ~20 segundos y verifica que todo esté `healthy`/`Up`:

```bash
docker compose ps
```

Salida esperada:

```
NAME       STATUS
nginx      Up
frontend   Up
express    Up
django     Up (healthy)
postgres   Up (healthy)
```

---

## 6. Aplicar migraciones de base de datos

La base de datos arranca vacía — hay que crear las tablas:

```bash
docker compose exec django python manage.py migrate
```

(Opcional) Si quieres cargar datos de ejemplo, revisa si existe un fixture/seed en
`backend-django/` antes de crear contenido manualmente vía Django admin o API.

---

## 7. Verificación

```bash
# Frontend
curl -I http://TU_IP_PUBLICA
# Esperado: HTTP/1.1 200 OK

# API (a través del proxy completo Nginx -> Express -> Django)
curl http://TU_IP_PUBLICA/api/servicios
# Esperado: [] o un JSON con datos, HTTP 200

curl http://TU_IP_PUBLICA/api/health
# Esperado: {"ok":true}
```

Abre `http://TU_IP_PUBLICA` en el navegador — deberías ver el sitio de Orion.

---

## 8. Auto-inicio al reiniciar el servidor (systemd)

```bash
sudo cp /opt/orion/.systemd/orion-compose.service /etc/systemd/system/
sudo nano /etc/systemd/system/orion-compose.service
# Verifica que WorkingDirectory=/opt/orion y User=<tu-usuario> sean correctos

sudo systemctl daemon-reload
sudo systemctl enable --now orion-compose.service
sudo systemctl status orion-compose.service
```

---

## Operaciones comunes

```bash
# Logs
docker compose logs -f
docker compose logs -f django

# Reiniciar un servicio
docker compose restart django

# Detener / levantar todo
docker compose down
docker compose up -d

# Backup de BD
docker compose exec postgres pg_dump -U postgres orion > backup_$(date +%Y%m%d).sql

# Restaurar BD
docker compose exec -T postgres psql -U postgres -d orion < backup_20260101.sql
```

---

## Troubleshooting

**`400 Bad Request` en `/api/*`**
`ALLOWED_HOSTS` de Django no incluye el host correcto. Verifica que `SERVER_IP` esté
seteado en `.env.production` y que `docker compose config` lo refleje:
```bash
docker compose config | grep ALLOWED_HOSTS
```

**`500` en cualquier endpoint que use la BD**
Revisa que `DB_SSL_REQUIRE=False` esté en `.env.production` — el Postgres del
docker-compose no tiene SSL habilitado.

**Puerto 80 ocupado**
```bash
sudo lsof -i :80
sudo systemctl stop apache2 nginx 2>/dev/null   # si hay un servidor web nativo corriendo
```

**Nginx no arranca / config inválida**
```bash
docker compose logs nginx
```

---

## Siguiente paso: dominio + SSL

Cuando tengas un dominio apuntando a la IP del servidor (registro DNS tipo A), se puede
agregar HTTPS con Let's Encrypt/Certbot. Avísame cuando llegues a ese punto y ajustamos
`nginx/conf.d/default.conf` y `ALLOWED_ORIGINS`/`SERVER_IP` para el dominio.
