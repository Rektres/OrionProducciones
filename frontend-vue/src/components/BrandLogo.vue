<script setup lang="ts">
defineProps<{
  name: string;
}>();
</script>

<template>
  <span class="brand-logo-icon" :class="`brand-logo--${name}`">
    <!-- Banco Santander (Llama roja emblemática) -->
    <svg v-if="name === 'santander'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#ec0000" fill-opacity="0.12" />
      <path d="M12 3C8.5 7 6.5 10 6.5 13.5c0 3 2.5 5.5 5.5 5.5s5.5-2.5 5.5-5.5c0-3.5-2-6.5-5.5-10.5z" fill="#ec0000" />
      <path d="M12 7.5c-1.8 2.2-2.8 4-2.8 5.8 0 1.5 1.2 2.8 2.8 2.8s2.8-1.3 2.8-2.8c0-1.8-1-3.6-2.8-5.8z" fill="#ffffff" />
    </svg>

    <!-- Entel (La icónica 'e' de telecomunicaciones con punto naranja) -->
    <svg v-else-if="name === 'entel'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#002eff" fill-opacity="0.1" />
      <path d="M14.5 12.5H9.5c0-1.4 1.1-2.5 2.5-2.5s2.5 1.1 2.5 2.5zm-5 1.2c0 1.4 1.1 2.5 2.5 2.5 1 0 1.8-.6 2.2-1.4h1.8C15.5 16.8 13.9 18 12 18c-2.8 0-5-2.2-5-5s2.2-5 5-5c2.8 0 5 2.2 5 5v1.2H9.5z" fill="#005cff" />
      <circle cx="16.5" cy="7.5" r="2.2" fill="#ff7900" />
    </svg>

    <!-- Viña Santa Rita (Racimo y copa de vino boutique) -->
    <svg v-else-if="name === 'santa-rita'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#8c1d40" fill-opacity="0.1" />
      <path d="M8 5h8v2.5c0 2-1.8 3.5-4 3.5s-4-1.5-4-3.5V5z" fill="#8c1d40" />
      <path d="M12 11v6m-3 2h6" stroke="#8c1d40" stroke-width="1.8" stroke-linecap="round" />
      <circle cx="9.5" cy="7.5" r="1" fill="#c5a880" />
      <circle cx="14.5" cy="7.5" r="1" fill="#c5a880" />
    </svg>

    <!-- Mallplaza (Estrella emblemática Mallplaza) -->
    <svg v-else-if="name === 'mallplaza'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#ff0055" fill-opacity="0.1" />
      <path d="M12 4l2.4 5.5 6 .5-4.5 3.9 1.4 5.8-5.3-3.1-5.3 3.1 1.4-5.8-4.5-3.9 6-.5L12 4z" fill="#ff0055" />
    </svg>

    <!-- BHP Escondida (Monograma Minero) -->
    <svg v-else-if="name === 'bhp'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <rect x="2" y="6" width="20" height="12" rx="3" fill="#ff5c00" />
      <text x="12" y="15" fill="#ffffff" font-size="8" font-weight="900" font-family="sans-serif" text-anchor="middle">BHP</text>
    </svg>

    <!-- Codelco (Sol / Cobre de Chile) -->
    <svg v-else-if="name === 'codelco'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9" fill="#d97706" />
      <circle cx="12" cy="12" r="5" fill="#ffffff" />
      <circle cx="12" cy="12" r="2.5" fill="#d97706" />
      <path d="M12 4v2.5m0 11V20M4 12h2.5m11 0H20" stroke="#ffffff" stroke-width="1.4" stroke-linecap="round" />
    </svg>

    <!-- Copec (Gota & Sol) -->
    <svg v-else-if="name === 'copec'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#0080ff" fill-opacity="0.1" />
      <path d="M12 3C8.5 7.5 6 11 6 14.5a6 6 0 0 0 12 0c0-3.5-2.5-7-6-11.5z" fill="#0080ff" />
      <circle cx="12" cy="14" r="3" fill="#facc15" />
    </svg>

    <!-- Lotus Producciones (Flor de loto de conciertos & festivales) -->
    <svg v-else-if="name === 'lotus'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#a855f7" fill-opacity="0.1" />
      <path d="M12 4c1.5 2.8 3.5 5.5 3.5 8 0 2-1.6 3.5-3.5 3.5S8.5 14 8.5 12c0-2.5 2-5.2 3.5-8z" fill="#a855f7" />
      <path d="M7 13.5c0-1.8 1.6-3.8 3.2-5 0 2 .8 3.6 1.8 4.8-1.2.8-2.8 1.2-5 .2z" fill="#ec4899" />
      <path d="M17 13.5c0-1.8-1.6-3.8-3.2-5 0 2-.8 3.6-1.8 4.8 1.2.8 2.8 1.2 5 .2z" fill="#ec4899" />
    </svg>

    <!-- Universidad de Chile (La U clásica) -->
    <svg v-else-if="name === 'uchile'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="3" width="18" height="18" rx="4" fill="#0033a0" />
      <path d="M7 6v6c0 2.8 2.2 5 5 5s5-2.2 5-5V6h-3v6c0 1.1-.9 2-2 2s-2-.9-2-2V6H7z" fill="#ffffff" />
    </svg>

    <!-- Red Bull Chile (Toros & Escenario) -->
    <svg v-else-if="name === 'redbull'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="6" fill="#fbbf24" />
      <path d="M4 14c2-1 4-1 6 1l2-2-2-2c-2 2-4 2-6 1v2zm16 0c-2-1-4-1-6 1l-2-2 2-2c2 2 4 2 6 1v2z" fill="#dc2626" />
    </svg>

    <!-- Gran Arena Monticello (Corona & Escenario) -->
    <svg v-else-if="name === 'monticello'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" fill="#1e1b4b" />
      <path d="M6 16l2-7 4 3.5 4-3.5 2 7H6z" fill="#eab308" />
      <circle cx="6" cy="7.5" r="1" fill="#eab308" />
      <circle cx="12" cy="11" r="1" fill="#eab308" />
      <circle cx="18" cy="7.5" r="1" fill="#eab308" />
    </svg>

    <!-- Espacio Riesco (Prisma de convenciones & eventos) -->
    <svg v-else-if="name === 'espacio-riesco'" width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#0284c7" fill-opacity="0.1" />
      <path d="M12 3l8 4.5v9l-8 4.5-8-4.5v-9l8-4.5z" fill="#0284c7" />
      <path d="M12 3v9l8-4.5M12 12l-8-4.5M12 12v9" stroke="#ffffff" stroke-width="1.2" />
    </svg>

    <!-- Fallback general -->
    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 8v8M8 12h8" />
    </svg>
  </span>
</template>

<style scoped>
.brand-logo-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.brand-pill:hover .brand-logo-icon {
  transform: scale(1.15) rotate(3deg);
}
</style>