<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  imagenUrl: string | null;
  deshabilitado?: boolean;
}>();

const emit = defineEmits<{
  subir: [archivo: File];
  quitar: [];
}>();

const TAMANO_MAX = 10 * 1024 * 1024;
const error = ref('');
const inputRef = ref<HTMLInputElement | null>(null);

const onChange = (e: Event) => {
  error.value = '';
  const archivo = (e.target as HTMLInputElement).files?.[0];
  if (!archivo) return;
  if (!archivo.type.startsWith('image/')) {
    error.value = 'El archivo debe ser una imagen.';
  } else if (archivo.size > TAMANO_MAX) {
    error.value = 'La imagen supera el tamaño máximo permitido (10MB).';
  } else {
    emit('subir', archivo);
  }
  if (inputRef.value) inputRef.value.value = '';
};
</script>

<template>
  <div>
    <div v-if="props.imagenUrl" class="card-cover rounded mb-2" style="height: 8rem; max-width: 12rem"
      :style="{ backgroundImage: `url('${props.imagenUrl}')` }"></div>
    <input ref="inputRef" type="file" accept="image/png,image/jpeg,image/webp,image/gif"
      class="form-control form-control-sm" :disabled="props.deshabilitado" @change="onChange" />
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
    <button v-if="props.imagenUrl" type="button" class="btn btn-outline-light btn-sm mt-2"
      :disabled="props.deshabilitado" @click="emit('quitar')">
      Quitar imagen
    </button>
  </div>
</template>
