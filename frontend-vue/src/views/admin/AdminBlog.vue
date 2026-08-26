<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref } from 'vue';
import { adminBlogService } from '@/services/adminBlog';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { Post, PostInput, Tag } from '@/types';

const posts = ref<Post[]>([]);
const tags = ref<Tag[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');
const guardadoOk = ref(false);
const busqueda = ref('');
const formEl = ref<HTMLElement | null>(null);
const nuevoTagNombre = ref('');

const filtrados = computed(() => {
  const q = busqueda.value.trim().toLowerCase();
  if (!q) return posts.value;
  return posts.value.filter((p) =>
    p.titulo.toLowerCase().includes(q) || p.estado.toLowerCase().includes(q));
});

const formVacio = (): PostInput => ({
  titulo: '',
  slug: '',
  extracto: '',
  contenido: '',
  estado: 'borrador',
  fecha_publicacion: null,
  tags: [],
});

const form = reactive<PostInput>(formVacio());

const cargar = async () => {
  [tags.value, posts.value] = await Promise.all([
    adminBlogService.listarTags(),
    adminBlogService.listar(),
  ]);
};

onMounted(cargar);

const enfocarForm = async () => {
  await nextTick();
  formEl.value?.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

const slugify = (texto: string) =>
  texto.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const onTituloInput = () => {
  if (!editandoId.value) form.slug = slugify(form.titulo);
};

const nuevo = async () => {
  Object.assign(form, formVacio());
  form.tags = [];
  editandoId.value = null;
  mostrarForm.value = true;
  error.value = '';
  guardadoOk.value = false;
  await enfocarForm();
};

const editar = async (p: Post) => {
  Object.assign(form, {
    titulo: p.titulo,
    slug: p.slug,
    extracto: p.extracto,
    contenido: p.contenido,
    estado: p.estado,
    fecha_publicacion: p.fecha_publicacion,
  });
  form.tags = (p.tags || []).map((t) => t.id);
  editandoId.value = p.id;
  mostrarForm.value = true;
  error.value = '';
  guardadoOk.value = false;
  await enfocarForm();
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
  guardadoOk.value = false;
};

const aplanarError = (e: any): string => {
  const data = e?.response?.data;
  if (!data) return 'Error guardando la pregunta.';
  if (typeof data === 'string') return data;
  return Object.values(data).flat().join(' ');
};

const guardar = async () => {
  guardando.value = true;
  error.value = '';
  guardadoOk.value = false;
  try {
    if (editandoId.value) {
      await adminBlogService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminBlogService.crear(form);
      editandoId.value = creado.id;
    }
    await cargar();
    guardadoOk.value = true;
    setTimeout(() => { guardadoOk.value = false; }, 2500);
  } catch (e) {
    error.value = aplanarError(e);
  } finally {
    guardando.value = false;
  }
};

const eliminar = async (p: Post) => {
  if (!confirm(`¿Eliminar la pregunta "${p.titulo}"?\n\nEsta acción no se puede deshacer.`)) return;
  await adminBlogService.eliminar(p.id);
  if (editandoId.value === p.id) cancelar();
  await cargar();
};

const subirImagen = async (archivo: File) => {
  if (!editandoId.value) return;
  await adminBlogService.subirImagen(editandoId.value, archivo);
  await cargar();
};

const quitarImagen = async () => {
  if (!editandoId.value) return;
  await adminBlogService.quitarImagen(editandoId.value);
  await cargar();
};

const postActual = () => posts.value.find((p) => p.id === editandoId.value) || null;

const agregarTag = async () => {
  const nombre = nuevoTagNombre.value.trim();
  if (!nombre) return;
  const tag = await adminBlogService.crearTag(nombre, slugify(nombre));
  tags.value.push(tag);
  form.tags.push(tag.id);
  nuevoTagNombre.value = '';
};
</script>

<template>
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
    <div>
      <h4 class="mb-0">Preguntas frecuentes</h4>
      <small class="text-secondary">{{ posts.length }} preguntas</small>
    </div>
    <div class="d-flex gap-2 flex-wrap">
      <input v-model="busqueda" type="search" class="form-control form-control-sm admin-toolbar-search"
        placeholder="Buscar por título o estado..." />
      <button type="button" class="btn btn-orion btn-sm" @click="nuevo">+ Nueva pregunta</button>
    </div>
  </div>

  <div v-if="mostrarForm" ref="formEl" class="card admin-card p-4 mb-4">
    <div class="d-flex justify-content-between align-items-start mb-3">
      <h5 class="mb-0">{{ editandoId ? 'Editar pregunta' : 'Nueva pregunta' }}</h5>
      <button type="button" class="btn-close" aria-label="Cerrar" @click="cancelar"></button>
    </div>
    <form class="row g-3" @submit.prevent="guardar">
      <div class="col-md-8">
        <label class="form-label">Pregunta *</label>
        <input v-model="form.titulo" type="text" required class="form-control" @input="onTituloInput" />
      </div>
      <div class="col-md-4">
        <label class="form-label">Slug *</label>
        <input v-model="form.slug" type="text" required class="form-control" />
      </div>
      <div class="col-12">
        <label class="form-label">Resumen *</label>
        <textarea v-model="form.extracto" required rows="2" class="form-control"></textarea>
      </div>
      <div class="col-12">
        <label class="form-label">Respuesta (HTML) *</label>
        <textarea v-model="form.contenido" required rows="8" class="form-control"></textarea>
        <div class="form-text">Se muestra dentro del acordeón en la página de FAQ. Acepta HTML simple.</div>
      </div>
      <div class="col-md-4">
        <label class="form-label">Estado *</label>
        <select v-model="form.estado" class="form-select">
          <option value="borrador">Borrador</option>
          <option value="revision">Revisión</option>
          <option value="publicado">Publicado</option>
        </select>
        <div class="form-text">Solo “Publicado” se ve en el sitio.</div>
      </div>
      <div class="col-md-8">
        <label class="form-label">Tags</label>
        <select v-model="form.tags" multiple class="form-select" size="4">
          <option v-for="t in tags" :key="t.id" :value="t.id">{{ t.nombre }}</option>
        </select>
        <div class="input-group input-group-sm mt-1">
          <input v-model="nuevoTagNombre" type="text" class="form-control" placeholder="Nuevo tag..."
            @keyup.enter="agregarTag" />
          <button type="button" class="btn btn-outline-secondary" @click="agregarTag">Agregar</button>
        </div>
      </div>

      <div class="col-12">
        <label class="form-label">Imagen (opcional)</label>
        <div v-if="!editandoId" class="text-secondary small">
          Guarda la pregunta primero y aquí podrás subir su imagen.
        </div>
        <ImagenUpload v-else :imagen-url="postActual()?.imagen_url ?? null"
          @subir="subirImagen" @quitar="quitarImagen" />
      </div>

      <div v-if="error" class="col-12"><div class="alert alert-danger py-2 mb-0">{{ error }}</div></div>

      <div class="col-12">
        <div class="admin-form-actions d-flex align-items-center gap-2">
          <button type="submit" class="btn btn-orion" :disabled="guardando">
            {{ guardando ? 'Guardando...' : 'Guardar' }}
          </button>
          <button type="button" class="btn btn-outline-secondary" @click="cancelar">Cerrar</button>
          <span v-if="guardadoOk" class="text-success small ms-1">✓ Cambios guardados</span>
        </div>
      </div>
    </form>
  </div>

  <div class="row g-3">
    <div v-for="p in filtrados" :key="p.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card admin-card-clickable hover-scale" @click="editar(p)">
        <div class="admin-thumb" :style="p.imagen_url ? { backgroundImage: `url('${p.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ p.titulo }}</h6>
          <span class="admin-badge-estado"
            :class="p.estado === 'publicado' ? 'text-success' : 'text-secondary'">{{ p.estado }}</span>
        </div>
        <div class="card-footer bg-transparent d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary btn-sm" @click.stop="editar(p)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(p)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!posts.length" class="col-12 text-secondary">Sin preguntas todavía. Crea la primera con “+ Nueva pregunta”.</div>
    <div v-else-if="!filtrados.length" class="col-12 text-secondary">Ninguna pregunta coincide con “{{ busqueda }}”.</div>
  </div>
</template>
