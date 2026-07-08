<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import WhatsAppButton from '@/components/WhatsAppButton.vue';
</script>

<template>
  <Navbar />
  <WhatsAppButton />
  <main>
    <router-view />
  </main>
  <Footer />
</template>
