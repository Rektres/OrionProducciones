import { ref, onMounted, onBeforeUnmount } from 'vue';

export function useReducedMotion() {
  const prefersReduced = ref(false);
  const query = window.matchMedia('(prefers-reduced-motion: reduce)');

  const update = () => { prefersReduced.value = query.matches; };

  onMounted(() => {
    update();
    query.addEventListener('change', update);
  });
  onBeforeUnmount(() => query.removeEventListener('change', update));

  return prefersReduced;
}
