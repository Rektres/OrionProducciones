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
const trabajando = ref(false);
const inputRef = ref<HTMLInputElement | null>(null);

// El padre hace la llamada al API; aca solo mostramos el estado mientras la
// promesa del emit se resuelve, para que el usuario sepa que algo ocurre.
const conEstado = async (fn: () => void) => {
  trabajando.value = true;
  try {
    fn();
    await new Promise((r) => setTimeout(r, 600));
  } finally {
    trabajando.value = false;
  }
};

const onChange = async (e: Event) => {
  error.value = '';
  const archivo = (e.target as HTMLInputElement).files?.[0];
  if (!archivo) return;
  if (!archivo.type.startsWith('image/')) {
    error.value = 'El archivo debe ser una imagen.';
  } else if (archivo.size > TAMANO_MAX) {
    error.value = 'La imagen supera el tamaño máximo permitido (10MB).';
  } else {
    await conEstado(() => emit('subir', archivo));
  }
  if (inputRef.value) inputRef.value.value = '';
};

const onQuitar = () => conEstado(() => emit('quitar'));
</script>

<template>
  <div>
    <div v-if="props.imagenUrl" class="card-cover rounded mb-2" style="height: 9rem; max-width: 14rem"
      :style="{ backgroundImage: `url('${props.imagenUrl}')` }"></div>
    <div v-else class="rounded mb-2 d-flex align-items-center justify-content-center text-secondary small"
      style="height: 9rem; max-width: 14rem; background: rgba(127,127,127,0.14)">
      Sin imagen
    </div>

    <input ref="inputRef" type="file" accept="image/png,image/jpeg,image/webp,image/gif"
      class="form-control form-control-sm" style="max-width: 22rem"
      :disabled="props.deshabilitado || trabajando" @change="onChange" />

    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
    <div v-else class="form-text">
      {{ trabajando ? 'Procesando imagen...' : 'JPG, PNG, WEBP o GIF · máx. 10MB' }}
    </div>

    <button v-if="props.imagenUrl" type="button" class="btn btn-outline-danger btn-sm mt-1"
      :disabled="props.deshabilitado || trabajando" @click="onQuitar">
      Quitar imagen
    </button>
  </div>
</template>
