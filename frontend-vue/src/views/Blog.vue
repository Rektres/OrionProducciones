<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import FadeInUp from '@/components/animations/FadeInUp.vue';
import ParticleBackground from '@/components/animations/ParticleBackground.vue';
import { blogService } from '@/services/blog';
import type { Post, Tag } from '@/types';

const posts = ref<Post[]>([]);
const tags = ref<Tag[]>([]);
const sel = ref<string | null>(null);
const page = ref(1);
const perPage = 9;

const cargar = async () => {
  posts.value = await blogService.getPosts(perPage, (page.value - 1) * perPage, sel.value || undefined);
};

const filtrar = async (slug: string | null) => {
  sel.value = slug;
  page.value = 1;
  await cargar();
};

onMounted(async () => {
  tags.value = await blogService.getTags();
  await cargar();
});
</script>

<template>
  <section class="py-5 text-center position-relative overflow-hidden">
    <ParticleBackground />
    <div class="container position-relative" style="z-index: 1">
      <h1 class="display-4 fw-bold">EL BLOG</h1>
      <p class="text-secondary">Consejos, tendencias e insights del equipo Orion</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container">
      <div class="d-flex flex-wrap gap-2 justify-content-center mb-4">
        <button class="btn btn-sm" :class="sel === null ? 'btn-orion' : 'btn-outline-light'" @click="filtrar(null)">Todos</button>
        <button v-for="t in tags" :key="t.id" class="btn btn-sm"
          :class="sel === t.slug ? 'btn-orion' : 'btn-outline-light'" @click="filtrar(t.slug)">
          {{ t.nombre }}
        </button>
      </div>
      <div class="row g-4">
        <div v-for="p in posts" :key="p.id" class="col-md-4">
          <FadeInUp>
            <RouterLink :to="`/blog/${p.slug}`" class="text-decoration-none">
              <div class="card h-100 bg-dark border-secondary">
                <div class="card-cover" style="height: 12rem" :style="{ backgroundImage: `url('${p.imagen_destacada}')` }"></div>
                <div class="card-body">
                  <h6 class="card-title">{{ p.titulo }}</h6>
                  <p class="card-text text-secondary small">{{ p.extracto }}</p>
                </div>
              </div>
            </RouterLink>
          </FadeInUp>
        </div>
      </div>
    </div>
  </section>
</template>
