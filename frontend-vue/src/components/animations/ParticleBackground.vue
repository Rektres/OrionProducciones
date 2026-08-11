<script setup lang="ts">
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { useReducedMotion } from '@/composables/useReducedMotion';
import { useTheme } from '@/composables/useTheme';

const props = withDefaults(defineProps<{ global?: boolean }>(), { global: false });

const canvas = ref<HTMLCanvasElement | null>(null);
const reducedMotion = useReducedMotion();
const { theme } = useTheme();
const fondoParticulas = computed(() => theme.value === 'light' ? 'rgba(255, 249, 245, 0.055)' : 'rgba(3, 8, 28, 0.09)');
const colorParticulas = computed(() => theme.value === 'light' ? 'rgba(205, 125, 143, 0.22)' : 'rgba(19, 214, 234, 0.16)');

let rafId = 0;

function start() {
  const c = canvas.value;
  if (!c) return;
  const ctx = c.getContext('2d');
  if (!ctx) return;

  const resize = () => {
    c.width = c.offsetWidth;
    c.height = c.offsetHeight;
  };
  resize();
  window.addEventListener('resize', resize);

  const count = Math.min(50, Math.floor(window.innerWidth / 20));
  const particles = Array.from({ length: count }, () => ({
    x: Math.random() * c.width,
    y: Math.random() * c.height,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    r: Math.random() * 2 + 1,
  }));

  const draw = () => {
    ctx.fillStyle = fondoParticulas.value;
    ctx.fillRect(0, 0, c.width, c.height);
    ctx.fillStyle = colorParticulas.value;
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = c.width;
      if (p.x > c.width) p.x = 0;
      if (p.y < 0) p.y = c.height;
      if (p.y > c.height) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
    rafId = requestAnimationFrame(draw);
  };
  draw();

  onBeforeUnmount(() => window.removeEventListener('resize', resize));
}

onMounted(() => {
  if (!reducedMotion.value) start();
});

onBeforeUnmount(() => cancelAnimationFrame(rafId));
</script>

<template>
  <canvas v-if="!reducedMotion" ref="canvas" class="particle-bg" :class="{ 'particle-bg-global': props.global }"></canvas>
</template>

<style scoped>
.particle-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  width: 100%;
  height: 100%;
}
.particle-bg-global {
  position: fixed;
  z-index: 0;
}
</style>
