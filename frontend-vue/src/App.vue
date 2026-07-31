<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import WhatsAppButton from '@/components/WhatsAppButton.vue';

const route = useRoute();
const esAdmin = computed(() => route.path.startsWith('/admin'));
</script>

<template>
  <Navbar v-if="!esAdmin" />
  <WhatsAppButton v-if="!esAdmin" />
  <main>
    <router-view />
  </main>
  <Footer v-if="!esAdmin" />
</template>
