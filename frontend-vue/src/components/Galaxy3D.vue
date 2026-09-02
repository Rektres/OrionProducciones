<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);
let animationFrameId: number | null = null;
let observer: IntersectionObserver | null = null;
let isVisible = true;

interface Star {
  arm: number;
  radius: number;
  angle: number;
  speed: number;
  size: number;
  color: string;
  alpha: number;
  zOffset: number;
}

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;

  // Setup High-DPI canvas
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let width = (canvas.clientWidth || 360);
  let height = (canvas.clientHeight || 360);

  const resize = () => {
    if (!canvas) return;
    width = canvas.clientWidth || 360;
    height = canvas.clientHeight || 360;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
  };
  resize();
  window.addEventListener('resize', resize);

  // Generate Galaxy Stars
  const numStars = 1400;
  const numArms = 2;
  const armSpread = 0.45;
  const maxRadius = 145;

  const starColors = [
    '#ffffff', // Core white
    '#38bdf8', // Neon cyan
    '#818cf8', // Electric indigo
    '#c084fc', // Nebula purple
    '#fde047', // Stellar gold
    '#60a5fa', // Celestial blue
  ];

  const stars: Star[] = [];
  for (let i = 0; i < numStars; i++) {
    const arm = i % numArms;
    // Radial distribution (more dense in center)
    const distFactor = Math.pow(Math.random(), 1.6);
    const radius = 8 + distFactor * maxRadius;
    
    // Logarithmic spiral angle + random spread
    const spiralAngle = (arm * (2 * Math.PI / numArms)) + (radius * 0.045);
    const spread = (Math.random() - 0.5) * armSpread * (radius / maxRadius + 0.3);
    const angle = spiralAngle + spread;
    
    // Closer stars revolve faster (Keplerian-like curve)
    const speed = 0.003 + (1 / (radius + 20)) * 0.12;
    
    const size = Math.random() < 0.85 ? (0.6 + Math.random() * 1.2) : (1.6 + Math.random() * 1.4);
    const color = starColors[Math.floor(Math.random() * starColors.length)];
    const alpha = 0.3 + Math.random() * 0.7;
    const zOffset = (Math.random() - 0.5) * 16 * (1 - distFactor * 0.5);

    stars.push({
      arm,
      radius,
      angle,
      speed,
      size,
      color,
      alpha,
      zOffset
    });
  }

  // 3D Tilt parameters (Increased pitch tilt + diagonal orientation matching reference)
  const tiltX = 74 * (Math.PI / 180); // Pitch tilt ~74 deg (more horizontal / elliptical disc)
  const tiltZ = -16 * (Math.PI / 180); // Diagonal orientation ~ -16 deg
  const cosTiltX = Math.cos(tiltX);
  const sinTiltX = Math.sin(tiltX);
  const cosTiltZ = Math.cos(tiltZ);
  const sinTiltZ = Math.sin(tiltZ);

  let rotation = 0;

  const render = () => {
    if (!isVisible) {
      animationFrameId = requestAnimationFrame(render);
      return;
    }

    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;

    // 1. Render Galactic Glow / Nebula background
    const bgGlow = ctx.createRadialGradient(cx, cy, 0, cx, cy, maxRadius * 1.2);
    bgGlow.addColorStop(0, 'rgba(56, 189, 248, 0.32)');
    bgGlow.addColorStop(0.2, 'rgba(99, 102, 241, 0.20)');
    bgGlow.addColorStop(0.5, 'rgba(168, 85, 247, 0.08)');
    bgGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
    
    ctx.fillStyle = bgGlow;
    ctx.beginPath();
    ctx.arc(cx, cy, maxRadius * 1.3, 0, Math.PI * 2);
    ctx.fill();

    // 2. Render Stars with 3D projection & diagonal slant
    rotation += 0.0035;

    for (let i = 0; i < stars.length; i++) {
      const star = stars[i];
      const curAngle = star.angle + rotation * (star.speed * 80);

      // 3D coordinates in galaxy plane
      const x0 = Math.cos(curAngle) * star.radius;
      const y0 = Math.sin(curAngle) * star.radius;
      const z0 = star.zOffset;

      // 1) Tilt around X axis (pitch)
      const x1 = x0;
      const y1 = y0 * cosTiltX - z0 * sinTiltX;
      const z1 = y0 * sinTiltX + z0 * cosTiltX;

      // 2) Rotate around Z axis (diagonal slant)
      const x2 = x1 * cosTiltZ - y1 * sinTiltZ;
      const y2 = x1 * sinTiltZ + y1 * cosTiltZ;

      const x2d = cx + x2;
      const y2d = cy + y2;
      const depthScale = 0.75 + ((z1 + maxRadius) / (maxRadius * 2)) * 0.5;

      ctx.beginPath();
      ctx.arc(x2d, y2d, Math.max(0.4, star.size * depthScale), 0, Math.PI * 2);
      ctx.fillStyle = star.color;
      ctx.globalAlpha = star.alpha * depthScale;
      ctx.fill();
    }

    // 3. Render Luminous Core
    const coreGlow = ctx.createRadialGradient(cx, cy, 0, cx, cy, 32);
    coreGlow.addColorStop(0, 'rgba(255, 255, 255, 1)');
    coreGlow.addColorStop(0.2, 'rgba(240, 249, 255, 0.9)');
    coreGlow.addColorStop(0.45, 'rgba(56, 189, 248, 0.6)');
    coreGlow.addColorStop(0.75, 'rgba(129, 140, 248, 0.25)');
    coreGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');

    ctx.globalAlpha = 1;
    ctx.fillStyle = coreGlow;
    ctx.beginPath();
    ctx.arc(cx, cy, 32, 0, Math.PI * 2);
    ctx.fill();

    // Central star spike / core lens flare
    ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
    ctx.beginPath();
    ctx.arc(cx, cy, 5.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
    animationFrameId = requestAnimationFrame(render);
  };

  // Optimize with IntersectionObserver to only render when in view
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      isVisible = entry.isIntersecting;
    });
  }, { threshold: 0.05 });
  observer.observe(canvas);

  render();

  onUnmounted(() => {
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    if (observer) observer.disconnect();
    window.removeEventListener('resize', resize);
  });
});
</script>

<template>
  <div class="galaxy-wrapper">
    <canvas ref="canvasRef" class="galaxy-canvas"></canvas>
  </div>
</template>

<style scoped>
.galaxy-wrapper {
  position: relative;
  width: 100%;
  max-width: 380px;
  aspect-ratio: 1 / 1;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(14, 21, 47, 0.6) 0%, rgba(7, 8, 20, 0) 70%);
}

.galaxy-canvas {
  width: 100%;
  height: 100%;
  display: block;
  filter: drop-shadow(0 0 24px rgba(56, 189, 248, 0.45));
}
</style>
