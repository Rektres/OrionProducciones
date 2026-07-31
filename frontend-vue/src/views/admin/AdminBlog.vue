<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { adminBlogService } from '@/services/adminBlog';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { Post, PostInput, Tag } from '@/types';

const posts = ref<Post[]>([]);
const tags = ref<Tag[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');
const nuevoTagNombre = ref('');

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

const nuevo = () => {
  Object.assign(form, formVacio());
  form.tags = [];
  editandoId.value = null;
  mostrarForm.value = true;
  error.value = '';
};

const editar = (p: Post) => {
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
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
};

const aplanarError = (e: any): string => {
  const data = e?.response?.data;
  if (!data) return 'Error guardando el post.';
  if (typeof data === 'string') return data;
  return Object.values(data).flat().join(' ');
};

const guardar = async () => {
  guardando.value = true;
  error.value = '';
  try {
    if (editandoId.value) {
      await adminBlogService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminBlogService.crear(form);
      editandoId.value = creado.id;
    }
    await cargar();
  } catch (e) {
    error.value = aplanarError(e);
  } finally {
    guardando.value = false;
  }
};

const eliminar = async (p: Post) => {
  if (!confirm(`¿Eliminar el post "${p.titulo}"?`)) return;
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
  const slug = nombre.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const tag = await adminBlogService.crearTag(nombre, slug);
  tags.value.push(tag);
  form.tags.push(tag.id);
  nuevoTagNombre.value = '';
};
</script>

<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h4 class="mb-0">Preguntas frecuentes</h4>
    <button type="button" class="btn btn-orion btn-sm" @click="nuevo">Nueva pregunta</button>
  </div>

  <div v-if="mostrarForm" class="card admin-card p-4 mb-4">
    <form class="row g-3" @submit.prevent="guardar">
      <div class="col-md-6">
        <label class="form-label">Título *</label>
        <input v-model="form.titulo" type="text" required class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Slug *</label>
        <input v-model="form.slug" type="text" required class="form-control" />
      </div>
      <div class="col-12">
        <label class="form-label">Extracto *</label>
        <textarea v-model="form.extracto" required rows="2" class="form-control"></textarea>
      </div>
      <div class="col-12">
        <label class="form-label">Contenido (HTML) *</label>
        <textarea v-model="form.contenido" required rows="8" class="form-control"></textarea>
      </div>
      <div class="col-md-4">
        <label class="form-label">Estado *</label>
        <select v-model="form.estado" class="form-select">
          <option value="borrador">Borrador</option>
          <option value="revision">Revisión</option>
          <option value="publicado">Publicado</option>
        </select>
      </div>
      <div class="col-md-8">
        <label class="form-label">Tags</label>
        <select v-model="form.tags" multiple class="form-select">
          <option v-for="t in tags" :key="t.id" :value="t.id">{{ t.nombre }}</option>
        </select>
        <div class="input-group input-group-sm mt-1">
          <input v-model="nuevoTagNombre" type="text" class="form-control" placeholder="Nuevo tag..." />
          <button type="button" class="btn btn-outline-light" @click="agregarTag">Agregar</button>
        </div>
      </div>
      <div class="col-12">
        <label class="form-label">Imagen destacada</label>
        <div v-if="!editandoId" class="text-secondary small">Guarda el post primero para poder subir una imagen.</div>
        <ImagenUpload v-else :imagen-url="postActual()?.imagen_url ?? null"
          @subir="subirImagen" @quitar="quitarImagen" />
      </div>
      <div v-if="error" class="col-12"><div class="alert alert-danger py-2 mb-0">{{ error }}</div></div>
      <div class="col-12 d-flex gap-2">
        <button type="submit" class="btn btn-orion" :disabled="guardando">
          {{ guardando ? 'Guardando...' : 'Guardar' }}
        </button>
        <button type="button" class="btn btn-outline-light" @click="cancelar">Cerrar</button>
      </div>
    </form>
  </div>

  <div class="row g-3">
    <div v-for="p in posts" :key="p.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card hover-scale" role="button" @click="editar(p)">
        <div class="card-cover rounded-top" style="height: 8rem"
          :style="p.imagen_url ? { backgroundImage: `url('${p.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ p.titulo }}</h6>
          <div class="small text-secondary">{{ p.estado }} · {{ p.fecha_publicacion || 'sin fecha' }}</div>
        </div>
        <div class="card-footer admin-card d-flex justify-content-between">
          <button type="button" class="btn btn-outline-light btn-sm" @click.stop="editar(p)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(p)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!posts.length" class="col-12 text-secondary">Sin posts todavía.</div>
  </div>
</template>
