# Orion Stage — Plataforma Web Corporativa & Panel de Administración

[![Producción](https://img.shields.io/badge/Producción-orionstage.cl-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://www.orionstage.cl)
[![Vue 3](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Django](https://img.shields.io/badge/Django_REST-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Express](https://img.shields.io/badge/Express-BFF-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Plataforma oficial desarrollada para **Orion Stage Producciones SpA**, productora técnica e integral de eventos corporativos, masivos, festivales y activaciones de marca en Chile.

🌐 **Sitio Web Oficial en Producción:** [https://www.orionstage.cl](https://www.orionstage.cl)

---

## 🏛 Arquitectura del Sistema

La solución implementa una **arquitectura desacoplada en tres capas (Three-Tier Architecture)** optimizada para alta disponibilidad, seguridad y experiencia fluida de usuario:

```text
                                  ┌─────────────────────────── ORION STAGE ──────────────────────────┐
                                  │                                                                  │
[Navegador / Cliente] ──▶ Nginx Reverse Proxy (:80 / :443) ──┬──▶ Frontend Vue 3 (SPA Pública & Admin)
                                                             │
                                                             └──▶ BFF Express Proxy (:3000)
                                                                        │
                                                                        └──▶ API Django REST (:8000) ──▶ PostgreSQL (:5432)
                                                                                    │
                                                                                    ├──▶ Notificaciones SMTP & WhatsApp
                                                                                    └──▶ Motor de Imágenes WebP
```

### Componentes Clave:
1. **Frontend SPA (Vue 3 + TypeScript):**
   * Diseñado bajo un concepto escénico *dark/luxury* que refleja la identidad de la productora.
   * Renderizado reactivo con Vite 5, Vue Router 4 y componentes modulares basados en Bootstrap 5 con variables CSS personalizadas.
   * Panel de administración interno (`/admin`) protegido para gestión del catálogo de servicios y portafolio de eventos.

2. **Capa BFF - Backend for Frontend (Node.js + Express + TypeScript):**
   * Actúa como proxy inteligente y capa de agregación (`http-proxy-middleware`).
   * Manejo granular de políticas CORS, rate limiting y sanitización de solicitudes previas al backend central.

3. **Backend Central (Python + Django 5 + Django REST Framework):**
   * API REST robusta que encapsula la lógica de negocio, validaciones y modelos de datos (`catalogo`, `servicios`, `eventos`, `cotizaciones`).
   * Autenticación segura mediante Tokens DRF para el panel de administración.
   * Procesamiento de correos electrónicos automáticos duales (confirmación para el cliente y ficha de lead para el productor).

4. **Base de Datos & Almacenamiento (PostgreSQL & WebP Engine):**
   * Persistencia relacional estructurada sobre PostgreSQL.
   * Motor propio de almacenamiento binario para imágenes con compresión WebP automática y entrega optimizada con cabeceras de caché inmutables.

---

## ✨ Características y Funcionalidades Destacadas

* 🌟 **Hero 3D Cover Flow:** Carrusel tridimensional interactivo con física de rotación y perspectiva de profundidad para exhibir los eventos principales.
* 🌌 **Galaxia WebGL Interactiva:** Fondo animado mediante canvas interactivo que reacciona sutilmente al desplazamiento del usuario.
* 📋 **Cotizador Inteligente con Validación Dinámica:**
  * Formateo automático de teléfonos chilenos (`+56 9 XXXX XXXX`).
  * Validación de correos corporativos y campos estructurados por tipo de evento.
  * Disparo de correos transaccionales automáticos vía SMTP y enlace directo a WhatsApp Business.
* 🔐 **Panel Administrativo Integral (`/admin`):**
  * Vista dual: alternador dinámico entre modo Tarjetas (*Cards*) y modo Lista/Tabla compacta.
  * Modales de edición fluida para creación y actualización de ítems sin recargar la página.
* 🔍 **Optimización SEO & Rendimiento:**
  * Metadatos dinámicos Open Graph y Twitter Cards.
  * Datos estructurados Schema.org (`EntertainmentBusiness` y `Event`).
  * Generación dinámica de `sitemap.xml` y `robots.txt`.

---

## 🛠 Ficha Técnica

| Área | Tecnologías |
|---|---|
| **Frontend** | Vue 3 (Composition API), TypeScript, Vite 5, Vue Router, Bootstrap 5, Axios, Canvas / WebGL |
| **BFF Proxy** | Node.js 20, Express, TypeScript, http-proxy-middleware, Helmet, CORS |
| **Backend** | Python 3.12, Django 5.1, Django REST Framework, Gunicorn, Pillow, psycopg3 |
| **Base de Datos** | PostgreSQL 16 (Supabase / Docker) |
| **Infraestructura** | Docker Compose, Nginx Reverse Proxy, Cloudflare SSL |

---

## 🔒 Confidencialidad y Código Propietario

> [!NOTE]
> El código fuente y la implementación interna de esta plataforma son de carácter **privado y confidencial**, al tratarse de un sistema desplegado en producción para un cliente corporativo activo.
>
> Este repositorio público se mantiene como **vitrina técnica de arquitectura y diseño de software**.

---

## 🌐 Visita el Proyecto en Vivo

Para conocer la experiencia en vivo, navegar por el catálogo y probar el cotizador:

👉 **[https://www.orionstage.cl](https://www.orionstage.cl)**
