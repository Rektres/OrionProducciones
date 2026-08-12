<script setup lang="ts">
import { onMounted, ref } from 'vue';
import DOMPurify from 'dompurify';
import { blogService } from '@/services/blog';
import type { Post } from '@/types';

const preguntas = ref<Post[]>([]);
const cargando = ref(true);

const limpiar = (html: string) => DOMPurify.sanitize(html);

onMounted(async () => {
  try {
    preguntas.value = await blogService.getPosts(50);
  } catch (e) {
    console.error('Error cargando FAQ:', e);
  } finally {
    cargando.value = false;
  }
});
</script>

<template>
  <section class="py-5 text-center position-relative overflow-hidden">
    <div class="container position-relative" style="z-index: 1">
      <h1 class="display-4 fw-bold">PREGUNTAS FRECUENTES</h1>
      <p class="text-secondary">Todo lo que necesitas saber antes de cotizar tu evento</p>
    </div>
  </section>

  <section class="py-4">
    <div class="container" style="max-width: 820px">
      <div v-if="cargando" class="text-center text-secondary py-5">Cargando preguntas...</div>
      <div v-else-if="!preguntas.length" class="text-center text-secondary py-5">
        Todavía no hay preguntas publicadas.
      </div>
      <div v-else class="accordion" id="faqAccordion">
        <div v-for="(p, idx) in preguntas" :key="p.id" class="accordion-item border-secondary mb-3">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button"
              data-bs-toggle="collapse" :data-bs-target="`#faq-${idx}`">
              {{ p.titulo }}
            </button>
          </h2>
          <div :id="`faq-${idx}`" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
            <div class="accordion-body text-secondary" v-html="limpiar(p.contenido)"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
