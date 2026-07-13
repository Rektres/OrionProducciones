<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useReducedMotion } from '@/composables/useReducedMotion';

const props = withDefaults(defineProps<{ delay?: number }>(), { delay: 0 });

const el = ref<HTMLElement | null>(null);
const visible = ref(false);
const reducedMotion = useReducedMotion();

let observer: IntersectionObserver | null = null;

onMounted(() => {
  if (reducedMotion.value) {
    visible.value = true;
    return;
  }
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        visible.value = true;
        observer?.disconnect();
      }
    },
    { rootMargin: '0px 0px -100px 0px' },
  );
  if (el.value) observer.observe(el.value);
});

onBeforeUnmount(() => observer?.disconnect());
</script>

<template>
  <div
    ref="el"
    class="fade-in-up"
    :class="{ 'is-visible': visible }"
    :style="{ transitionDelay: `${props.delay}s` }"
  >
    <slot />
  </div>
</template>

<style scoped>
.fade-in-up {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in-up.is-visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
