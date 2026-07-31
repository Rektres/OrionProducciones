<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { adminPortafolioService } from '@/services/adminPortafolio';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { Evento, EventoInput, EventoTipo, FotoEvento } from '@/types';

const eventos = ref<Evento[]>([]);
const tipos = ref<EventoTipo[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');

const fotos = ref<FotoEvento[]>([]);
const subiendoFoto = ref(false);

const mostrarTipos = ref(false);
const nuevoTipoNombre = ref('');

const formVacio = (): EventoInput => ({
  nombre: '',
  slug: '',
  tipo: null,
  cliente: '',
  descripcion_corta: '',
  descripcion_larga: '',
  fecha_realizacion: '',
  lugar: '',
  asistentes: null,
  destacado: false,
  publicado: true,
  orden: 0,
});

const form = reactive<EventoInput>(formVacio());

const cargar = async () => {
  [tipos.value, eventos.value] = await Promise.all([
    adminPortafolioService.listarTipos(),
    adminPortafolioService.listar(),
  ]);
};

onMounted(cargar);

const cargarFotos = async (eventoId: string) => {
  fotos.value = await adminPortafolioService.listarFotos(eventoId);
};

const nuevo = () => {
  Object.assign(form, formVacio());
  editandoId.value = null;
  fotos.value = [];
  mostrarForm.value = true;
  error.value = '';
};

const editar = async (ev: Evento) => {
  Object.assign(form, {
    nombre: ev.nombre,
    slug: ev.slug,
    tipo: ev.tipo,
    cliente: ev.cliente,
    descripcion_corta: ev.descripcion_corta,
    descripcion_larga: ev.descripcion_larga,
    fecha_realizacion: ev.fecha_realizacion,
    lugar: ev.lugar,
    asistentes: ev.asistentes,
    destacado: ev.destacado,
    publicado: ev.publicado,
    orden: ev.orden,
  });
  editandoId.value = ev.id;
  mostrarForm.value = true;
  error.value = '';
  await cargarFotos(ev.id);
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
  fotos.value = [];
};

const aplanarError = (e: any): string => {
  const data = e?.response?.data;
  if (!data) return 'Error guardando el evento.';
  if (typeof data === 'string') return data;
  return Object.values(data).flat().join(' ');
};

const guardar = async () => {
  guardando.value = true;
  error.value = '';
  try {
    if (editandoId.value) {
      await adminPortafolioService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminPortafolioService.crear(form);
      editandoId.value = creado.id;
      await cargarFotos(creado.id);
    }
    await cargar();
  } catch (e) {
    error.value = aplanarError(e);
  } finally {
    guardando.value = false;
  }
};

const eliminar = async (ev: Evento) => {
  if (!confirm(`¿Eliminar el evento "${ev.nombre}"?`)) return;
  await adminPortafolioService.eliminar(ev.id);
  if (editandoId.value === ev.id) cancelar();
  await cargar();
};

const subirImagen = async (archivo: File) => {
  if (!editandoId.value) return;
  await adminPortafolioService.subirImagen(editandoId.value, archivo);
  await cargar();
};

const quitarImagen = async () => {
  if (!editandoId.value) return;
  await adminPortafolioService.quitarImagen(editandoId.value);
  await cargar();
};

const eventoActual = () => eventos.value.find((e) => e.id === editandoId.value) || null;

const agregarFoto = async (e: Event) => {
  if (!editandoId.value) return;
  const archivo = (e.target as HTMLInputElement).files?.[0];
  if (!archivo) return;
  subiendoFoto.value = true;
  try {
    await adminPortafolioService.agregarFoto(editandoId.value, archivo);
    await cargarFotos(editandoId.value);
  } finally {
    subiendoFoto.value = false;
    (e.target as HTMLInputElement).value = '';
  }
};

const eliminarFoto = async (foto: FotoEvento) => {
  if (!confirm('¿Eliminar esta foto de la galería?')) return;
  await adminPortafolioService.eliminarFoto(foto.id);
  if (editandoId.value) await cargarFotos(editandoId.value);
};

const slugify = (texto: string) =>
  texto.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const agregarTipo = async () => {
  const nombre = nuevoTipoNombre.value.trim();
  if (!nombre) return;
  await adminPortafolioService.crearTipo(nombre, slugify(nombre));
  nuevoTipoNombre.value = '';
  tipos.value = await adminPortafolioService.listarTipos();
};

const eliminarTipo = async (t: EventoTipo) => {
  if (!confirm(`¿Eliminar el tipo "${t.nombre}"? Los eventos que lo usen quedarán sin tipo.`)) return;
  await adminPortafolioService.eliminarTipo(t.id);
  await cargar();
};
</script>

<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h4 class="mb-0">Portafolio</h4>
    <button type="button" class="btn btn-orion btn-sm" @click="nuevo">Nuevo evento</button>
  </div>

  <div class="card admin-card p-3 mb-4">
    <div class="d-flex justify-content-between align-items-center" style="cursor: pointer" @click="mostrarTipos = !mostrarTipos">
      <h6 class="mb-0">Tipos de evento</h6>
      <span class="text-secondary">{{ mostrarTipos ? '▲' : '▼' }}</span>
    </div>
    <div v-if="mostrarTipos" class="mt-3">
      <ul class="list-group list-group-flush mb-2">
        <li v-for="t in tipos" :key="t.id"
          class="list-group-item admin-card text-white d-flex justify-content-between align-items-center px-0">
          {{ t.nombre }}
          <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminarTipo(t)">Eliminar</button>
        </li>
        <li v-if="!tipos.length" class="list-group-item admin-card text-secondary px-0">Sin tipos todavía.</li>
      </ul>
      <div class="input-group input-group-sm">
        <input v-model="nuevoTipoNombre" type="text" class="form-control" placeholder="Nuevo tipo..."
          @keyup.enter="agregarTipo" />
        <button type="button" class="btn btn-outline-light" @click="agregarTipo">Agregar</button>
      </div>
    </div>
  </div>

  <div v-if="mostrarForm" class="card admin-card p-4 mb-4">
    <form class="row g-3" @submit.prevent="guardar">
      <div class="col-md-6">
        <label class="form-label">Nombre *</label>
        <input v-model="form.nombre" type="text" required class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Slug *</label>
        <input v-model="form.slug" type="text" required class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Tipo</label>
        <select v-model="form.tipo" class="form-select">
          <option :value="null">Sin tipo</option>
          <option v-for="t in tipos" :key="t.id" :value="t.id">{{ t.nombre }}</option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label">Cliente *</label>
        <input v-model="form.cliente" type="text" required class="form-control" />
      </div>
      <div class="col-12">
        <label class="form-label">Descripción corta *</label>
        <textarea v-model="form.descripcion_corta" required rows="2" class="form-control"></textarea>
      </div>
      <div class="col-12">
        <label class="form-label">Descripción larga *</label>
        <textarea v-model="form.descripcion_larga" required rows="4" class="form-control"></textarea>
      </div>
      <div class="col-md-4">
        <label class="form-label">Fecha de realización *</label>
        <input v-model="form.fecha_realizacion" type="date" required class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label">Lugar *</label>
        <input v-model="form.lugar" type="text" required class="form-control" />
      </div>
      <div class="col-md-4">
        <label class="form-label">Asistentes</label>
        <input v-model.number="form.asistentes" type="number" class="form-control" />
      </div>
      <div class="col-md-2">
        <label class="form-label">Orden</label>
        <input v-model.number="form.orden" type="number" class="form-control" />
      </div>
      <div class="col-md-3 d-flex align-items-end">
        <div class="form-check">
          <input v-model="form.destacado" type="checkbox" class="form-check-input" id="eventoDestacado" />
          <label class="form-check-label" for="eventoDestacado">Destacado</label>
        </div>
      </div>
      <div class="col-md-3 d-flex align-items-end">
        <div class="form-check">
          <input v-model="form.publicado" type="checkbox" class="form-check-input" id="eventoPublicado" />
          <label class="form-check-label" for="eventoPublicado">Publicado</label>
        </div>
      </div>

      <div class="col-12">
        <label class="form-label">Imagen destacada</label>
        <div v-if="!editandoId" class="text-secondary small">Guarda el evento primero para poder subir una imagen.</div>
        <ImagenUpload v-else :imagen-url="eventoActual()?.imagen_url ?? null"
          @subir="subirImagen" @quitar="quitarImagen" />
      </div>

      <div v-if="editandoId" class="col-12">
        <label class="form-label">Galería</label>
        <div class="d-flex flex-wrap gap-3 mb-2">
          <div v-for="f in fotos" :key="f.id" class="position-relative">
            <div class="card-cover rounded" style="height: 6rem; width: 6rem"
              :style="f.imagen_url ? { backgroundImage: `url('${f.imagen_url}')` } : {}"></div>
            <button type="button" class="btn btn-outline-danger btn-sm position-absolute top-0 end-0"
              @click="eliminarFoto(f)">×</button>
          </div>
        </div>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif"
          class="form-control form-control-sm" :disabled="subiendoFoto" @change="agregarFoto" />
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
    <div v-for="ev in eventos" :key="ev.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card hover-scale" role="button" @click="editar(ev)">
        <div class="card-cover rounded-top" style="height: 8rem"
          :style="ev.imagen_url ? { backgroundImage: `url('${ev.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ ev.nombre }}</h6>
          <div class="small text-secondary">{{ ev.tipo_slug || 'sin tipo' }} · {{ ev.fecha_realizacion }}</div>
          <div class="small text-secondary">{{ ev.publicado ? 'Publicado' : 'Sin publicar' }}</div>
        </div>
        <div class="card-footer admin-card d-flex justify-content-between">
          <button type="button" class="btn btn-outline-light btn-sm" @click.stop="editar(ev)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(ev)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!eventos.length" class="col-12 text-secondary">Sin eventos todavía.</div>
  </div>
</template>
