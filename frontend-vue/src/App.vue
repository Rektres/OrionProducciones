<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import WhatsAppButton from '@/components/WhatsAppButton.vue';
import ConsentimientoCookies from '@/components/ConsentimientoCookies.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';
import { analiticaConfigurada, cargarAnalitica, requiereConsentimiento } from '@/composables/useAnalitica';

const route = useRoute();
const esAdmin = computed(() => route.path.startsWith('/admin'));

// Plausible es cookieless: parte de inmediato. GA4 espera al banner.
if (analiticaConfigurada && !requiereConsentimiento) cargarAnalitica();
</script>

<template>
  <div class="site-shell" :class="{ 'site-shell-admin': esAdmin }">
    <ParticleBackground v-if="!esAdmin" global />
    <Navbar v-if="!esAdmin" />
    <WhatsAppButton v-if="!esAdmin" />
    <main class="site-content">
      <router-view />
    </main>
    <Footer v-if="!esAdmin" />
    <ConsentimientoCookies />
  </div>
</template>
