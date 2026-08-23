<script setup lang="ts">
import { RouterLink } from 'vue-router';
const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const whatsappUrl = `https://wa.me/${numero}`;
const instagramUrl = import.meta.env.VITE_INSTAGRAM_URL || '#';
const linkedinUrl = import.meta.env.VITE_LINKEDIN_URL || '#';
// Si no estan configurados no se muestran: mejor omitir el dato que publicar uno falso.
const email = import.meta.env.VITE_CONTACT_EMAIL || '';
const direccion = import.meta.env.VITE_CONTACT_DIRECCION || 'Santiago, Chile';
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
            <li><RouterLink class="link-secondary text-decoration-none" to="/faq">Preguntas frecuentes</RouterLink></li>
            <li><RouterLink class="link-secondary text-decoration-none" to="/quienes-somos">Quiénes somos</RouterLink></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h6 class="fw-semibold">Contacto</h6>
          <ul class="list-unstyled small text-secondary">
            <li>
              <a class="link-secondary text-decoration-none" :href="whatsappUrl" target="_blank" rel="noopener noreferrer">
                +{{ numero }}
              </a>
            </li>
            <li v-if="email">
              <a class="link-secondary text-decoration-none" :href="`mailto:${email}`">{{ email }}</a>
            </li>
            <li>{{ direccion }}</li>
          </ul>
          <div class="d-flex gap-3 mt-3">
            <a :href="instagramUrl" target="_blank" rel="noopener noreferrer" class="link-secondary" aria-label="Instagram">
              <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
              </svg>
            </a>
            <a :href="linkedinUrl" target="_blank" rel="noopener noreferrer" class="link-secondary" aria-label="LinkedIn">
              <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
              </svg>
            </a>
            <a :href="whatsappUrl" target="_blank" rel="noopener noreferrer" class="link-secondary" aria-label="WhatsApp">
              <svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.198-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.198-.1-.836-.308-1.592-.985-.588-.526-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.198-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.203.84.325 1.129.416.475.152.904.129 1.246.08.38-.058 1.171-.48 1.336-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
      <hr class="border-secondary" />
      <p class="text-center text-secondary small mb-0">
        © 2026 Todos los derechos reservados | Desarrollado por Mateo Araneda Medina
        · <RouterLink class="link-secondary" to="/terminos-y-condiciones">Términos y condiciones</RouterLink>
        · <RouterLink class="link-secondary" to="/politica-de-privacidad">Política de privacidad</RouterLink>
      </p>
    </div>
  </footer>
</template>
