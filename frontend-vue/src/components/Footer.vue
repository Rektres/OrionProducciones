<script setup lang="ts">
import { RouterLink } from 'vue-router';
const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
</script>

<template>
  <footer class="border-top border-secondary-subtle mt-5 py-5">
    <div class="container">
      <div class="row g-4">
        <div class="col-md-4">
          <img src="/logo.png" alt="Orión Stage" height="56" class="mb-2" />
          <p class="text-secondary small">
            Creamos experiencias inolvidables. Desde lo corporativo hasta lo más social.
          </p>
        </div>
        <div class="col-md-4">
          <h6 class="fw-semibold">Sitio</h6>
          <ul class="list-unstyled small">
            <li><RouterLink class="link-secondary text-decoration-none" to="/">Inicio</RouterLink></li>
            <li><RouterLink class="link-secondary text-decoration-none" to="/servicios">Servicios</RouterLink></li>
            <li><RouterLink class="link-secondary text-decoration-none" to="/portafolio">Portafolio</RouterLink></li>
            <li><RouterLink class="link-secondary text-decoration-none" to="/blog">Blog</RouterLink></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h6 class="fw-semibold">Contacto</h6>
          <ul class="list-unstyled small text-secondary">
            <li>
              <a class="link-secondary text-decoration-none" :href="`https://wa.me/${numero}`" target="_blank" rel="noopener noreferrer">
                +{{ numero }}
              </a>
            </li>
            <li>Santiago, Chile</li>
          </ul>
        </div>
      </div>
      <hr class="border-secondary" />
      <p class="text-center text-secondary small mb-0">
        © 2026 Todos los derechos reservados | Desarrollado por Mateo Araneda Medina
      </p>
    </div>
  </footer>
</template>
