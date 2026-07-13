<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useReducedMotion } from '@/composables/useReducedMotion';

const canvas = ref<HTMLCanvasElement | null>(null);
const reducedMotion = useReducedMotion();

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
    ctx.fillStyle = 'rgba(3, 8, 28, 0.1)';
    ctx.fillRect(0, 0, c.width, c.height);
    ctx.fillStyle = 'rgba(19, 214, 234, 0.15)';
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
  <canvas v-if="!reducedMotion" ref="canvas" class="particle-bg"></canvas>
</template>

<style scoped>
.particle-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  width: 100%;
  height: 100%;
}
</style>
