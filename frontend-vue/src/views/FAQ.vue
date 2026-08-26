<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue';
import DOMPurify from 'dompurify';
import { blogService } from '@/services/blog';
import type { Post } from '@/types';

const preguntas = ref<Post[]>([]);
const cargando = ref(true);

const limpiar = (html: string) => DOMPurify.sanitize(html);

const inyectarSchemaFaq = (lista: Post[]) => {
  if (!lista.length) return;
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: lista.map((p) => ({
      '@type': 'Question',
      name: p.titulo,
      acceptedAnswer: {
        '@type': 'Answer',
        text: p.contenido.replace(/<[^>]*>/g, '').trim(),
      },
    })),
  };
  let scriptEl = document.getElementById('faq-schema-jsonld') as HTMLScriptElement | null;
  if (!scriptEl) {
    scriptEl = document.createElement('script');
    scriptEl.id = 'faq-schema-jsonld';
    scriptEl.type = 'application/ld+json';
    document.head.appendChild(scriptEl);
  }
  scriptEl.textContent = JSON.stringify(schema);
};

onMounted(async () => {
  try {
    preguntas.value = await blogService.getPosts(50);
    inyectarSchemaFaq(preguntas.value);
  } catch (e) {
    console.error('Error cargando FAQ:', e);
  } finally {
    cargando.value = false;
  }
});

onBeforeUnmount(() => {
  const scriptEl = document.getElementById('faq-schema-jsonld');
  if (scriptEl) scriptEl.remove();
});
</script>

<template>
  <section class="pt-4 pb-2 text-center position-relative overflow-hidden">
    <div class="container position-relative" style="z-index: 1">
      <p class="eyebrow justify-content-center"><span></span> AYUDA Y RESPUESTAS</p>
      <h1 class="display-4 fw-bold">PREGUNTAS FRECUENTES</h1>
      <p class="text-secondary" style="max-width: 600px; margin: 0 auto;">Todo lo que necesitas saber sobre nuestra logística, tecnología de sonido, iluminación y proceso de contratación.</p>
    </div>
  </section>

  <section class="py-4 pb-5">
    <div class="container" style="max-width: 820px">
      <div v-if="cargando" class="text-center text-secondary py-5">
        <div class="spinner-border text-info" role="status"></div>
        <p class="mt-3">Cargando preguntas frecuentes...</p>
      </div>
      <div v-else-if="!preguntas.length" class="text-center text-secondary py-5">
        Todavía no hay preguntas publicadas.
      </div>
      <div v-else class="accordion faq-accordion" id="faqAccordion">
        <div v-for="(p, idx) in preguntas" :key="p.id" class="accordion-item faq-item mb-3">
          <h2 class="accordion-header">
            <button
              class="accordion-button collapsed faq-button"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="`#faq-${idx}`"
            >
              {{ p.titulo }}
            </button>
          </h2>
          <div :id="`faq-${idx}`" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
            <div class="accordion-body faq-body text-secondary" v-html="limpiar(p.contenido)"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq-item {
  border: 1px solid var(--bs-border-color);
  border-radius: 14px !important;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.faq-item:hover {
  border-color: rgba(34, 211, 238, 0.3);
}
.faq-button {
  font-family: var(--shell-display);
  font-weight: 700;
  font-size: 16px;
  padding: 18px 20px;
  color: var(--bs-body-color);
  background: transparent !important;
  box-shadow: none !important;
}
.faq-button:not(.collapsed) {
  color: var(--orion-primary);
  border-bottom: 1px solid var(--bs-border-color);
}
.faq-body {
  padding: 18px 20px;
  line-height: 1.75;
  font-size: 14px;
}
</style>

