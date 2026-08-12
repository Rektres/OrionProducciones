<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import WhatsAppButton from '@/components/WhatsAppButton.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';

const route = useRoute();
const esAdmin = computed(() => route.path.startsWith('/admin'));
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
  </div>
</template>
