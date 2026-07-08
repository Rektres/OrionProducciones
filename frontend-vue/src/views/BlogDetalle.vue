<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import DOMPurify from 'dompurify';
import { blogService } from '@/services/blog';
import type { Post } from '@/types';

const route = useRoute();
const post = ref<Post | null>(null);
const loading = ref(true);

const contenidoLimpio = computed(() => (post.value ? DOMPurify.sanitize(post.value.contenido) : ''));

onMounted(async () => {
  try {
    post.value = await blogService.getPostBySlug(String(route.params.slug));
  } catch (e) {
    post.value = null;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading" class="container py-5 text-center text-secondary">Cargando artículo...</div>
  <div v-else-if="!post" class="container py-5 text-center text-secondary">Artículo no encontrado</div>
  <template v-else>
    <div class="card-cover d-flex align-items-end" style="height: 22rem"
      :style="{ backgroundImage: `url('${post.imagen_destacada}')` }">
      <div class="container p-4" style="background: linear-gradient(0deg, rgba(0,0,0,0.85), transparent)">
        <h1 class="text-white">{{ post.titulo }}</h1>
      </div>
    </div>
    <div class="container py-5" style="max-width: 760px">
      <div class="d-flex flex-wrap gap-2 mb-4">
        <span v-for="t in post.tags" :key="t.id" class="badge text-bg-warning">{{ t.nombre }}</span>
      </div>
      <article class="text-secondary" v-html="contenidoLimpio"></article>
    </div>
  </template>
</template>
