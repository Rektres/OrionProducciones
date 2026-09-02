<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { adminPortafolioService } from '@/services/adminPortafolio';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { Evento, EventoInput, EventoTipo, FotoEvento } from '@/types';

const eventos = ref<Evento[]>([]);
const tipos = ref<EventoTipo[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');
const guardadoOk = ref(false);
const busqueda = ref('');
const vista = ref<'cards' | 'lista'>('cards');

const fotos = ref<FotoEvento[]>([]);
const subiendoFoto = ref(false);

const mostrarTipos = ref(false);
const nuevoTipoNombre = ref('');

const filtrados = computed(() => {
  const q = busqueda.value.trim().toLowerCase();
  if (!q) return eventos.value;
  return eventos.value.filter((e) =>
    e.nombre.toLowerCase().includes(q) ||
    e.cliente.toLowerCase().includes(q) ||
    (e.tipo_slug || '').toLowerCase().includes(q));
});

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

const slugify = (texto: string) =>
  texto.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const onNombreInput = () => {
  if (!editandoId.value) form.slug = slugify(form.nombre);
};

const nuevo = () => {
  Object.assign(form, formVacio());
  editandoId.value = null;
  fotos.value = [];
  mostrarForm.value = true;
  error.value = '';
  guardadoOk.value = false;
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
  guardadoOk.value = false;
  await cargarFotos(ev.id);
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
  fotos.value = [];
  guardadoOk.value = false;
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
  guardadoOk.value = false;
  try {
    if (editandoId.value) {
      await adminPortafolioService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminPortafolioService.crear(form);
      editandoId.value = creado.id;
      await cargarFotos(creado.id);
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

const eliminar = async (ev: Evento) => {
  if (!confirm(`¿Eliminar el evento "${ev.nombre}"?\n\nSe eliminarán también sus fotos de galería. Esta acción no se puede deshacer.`)) return;
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
  const input = e.target as HTMLInputElement;
  const archivos = Array.from(input.files ?? []);
  if (!archivos.length) return;
  subiendoFoto.value = true;
  try {
    for (const archivo of archivos) {
      await adminPortafolioService.agregarFoto(editandoId.value, archivo);
    }
    await cargarFotos(editandoId.value);
  } catch (err) {
    error.value = aplanarError(err);
  } finally {
    subiendoFoto.value = false;
    input.value = '';
  }
};

const eliminarFoto = async (foto: FotoEvento) => {
  if (!confirm('¿Eliminar esta foto de la galería?')) return;
  await adminPortafolioService.eliminarFoto(foto.id);
  if (editandoId.value) await cargarFotos(editandoId.value);
};

const agregarTipo = async () => {
  const nombre = nuevoTipoNombre.value.trim();
  if (!nombre) return;
  await adminPortafolioService.crearTipo(nombre, slugify(nombre));
  nuevoTipoNombre.value = '';
  tipos.value = await adminPortafolioService.listarTipos();
};

const eliminarTipo = async (t: EventoTipo) => {
  if (!confirm(`¿Eliminar el tipo "${t.nombre}"?\n\nLos eventos que lo usen quedarán sin tipo.`)) return;
  await adminPortafolioService.eliminarTipo(t.id);
  await cargar();
};
</script>

<template>
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
    <div>
      <h4 class="mb-0">Portafolio</h4>
      <small class="text-secondary">{{ eventos.length }} eventos</small>
    </div>
    <div class="d-flex gap-2 flex-wrap align-items-center">
      <input v-model="busqueda" type="search" class="form-control form-control-sm admin-toolbar-search"
        placeholder="Buscar por nombre, cliente o tipo..." />

      <!-- Toggle Vista Cards / Lista -->
      <div class="btn-group btn-group-sm" role="group" aria-label="Cambiar vista">
        <button
          type="button"
          class="btn"
          :class="vista === 'cards' ? 'btn-primary' : 'btn-outline-secondary'"
          title="Vista en tarjetas"
          @click="vista = 'cards'"
        >
          ⊞ Tarjetas
        </button>
        <button
          type="button"
          class="btn"
          :class="vista === 'lista' ? 'btn-primary' : 'btn-outline-secondary'"
          title="Vista en lista"
          @click="vista = 'lista'"
        >
          ☰ Lista
        </button>
      </div>

      <button type="button" class="btn btn-orion btn-sm" @click="nuevo">+ Nuevo evento</button>
    </div>
  </div>

  <div class="card admin-card p-3 mb-4">
    <div class="d-flex justify-content-between align-items-center admin-card-clickable"
      @click="mostrarTipos = !mostrarTipos">
      <h6 class="mb-0">Tipos de evento <span class="text-secondary fw-normal">({{ tipos.length }})</span></h6>
      <span class="text-secondary">{{ mostrarTipos ? '▲' : '▼' }}</span>
    </div>
    <div v-if="mostrarTipos" class="mt-3">
      <ul class="list-group list-group-flush mb-2">
        <li v-for="t in tipos" :key="t.id"
          class="list-group-item d-flex justify-content-between align-items-center px-0">
          {{ t.nombre }}
          <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminarTipo(t)">Eliminar</button>
        </li>
        <li v-if="!tipos.length" class="list-group-item text-secondary px-0">Sin tipos todavía.</li>
      </ul>
      <div class="input-group input-group-sm">
        <input v-model="nuevoTipoNombre" type="text" class="form-control" placeholder="Nuevo tipo..."
          @keyup.enter="agregarTipo" />
        <button type="button" class="btn btn-outline-secondary" @click="agregarTipo">Agregar</button>
      </div>
    </div>
  </div>

  <!-- MODAL DE CREACIÓN / EDICIÓN DE EVENTO -->
  <div
    v-if="mostrarForm"
    class="modal fade show d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.75); z-index: 1060;"
    @click.self="cancelar"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
      <div class="modal-content admin-card">
        <div class="modal-header border-bottom border-secondary border-opacity-25 pb-3">
          <h5 class="modal-title mb-0">{{ editandoId ? 'Editar evento' : 'Nuevo evento' }}</h5>
          <button type="button" class="btn-close" aria-label="Cerrar" @click="cancelar"></button>
        </div>
        <div class="modal-body p-4">
          <form id="formEventoModal" class="row g-3" @submit.prevent="guardar">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Nombre *</label>
              <input v-model="form.nombre" type="text" required class="form-control" placeholder="Ej: Aniversario BCI 2026" @input="onNombreInput" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Slug (URL) *</label>
              <input v-model="form.slug" type="text" required class="form-control" />
              <div class="form-text">{{ editandoId ? 'Cambiarlo altera la URL pública del evento.' : 'Se sugiere solo desde el nombre.' }}</div>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Tipo</label>
              <select v-model="form.tipo" class="form-select">
                <option :value="null">Sin tipo</option>
                <option v-for="t in tipos" :key="t.id" :value="t.id">{{ t.nombre }}</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Cliente *</label>
              <input v-model="form.cliente" type="text" required class="form-control" placeholder="Ej: Banco BCI" />
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Descripción corta *</label>
              <textarea v-model="form.descripcion_corta" required rows="2" class="form-control" placeholder="Resumen para tarjetas y vistas previas..."></textarea>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Descripción larga *</label>
              <textarea v-model="form.descripcion_larga" required rows="4" class="form-control" placeholder="Detalle exhaustivo de la producción, montaje y experiencia..."></textarea>
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Fecha de realización *</label>
              <input v-model="form.fecha_realizacion" type="date" required class="form-control" />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Lugar / Recinto *</label>
              <input v-model="form.lugar" type="text" required class="form-control" placeholder="Ej: Espacio Riesco, Santiago" />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Cantidad de Asistentes</label>
              <input v-model.number="form.asistentes" type="number" class="form-control" placeholder="Ej: 1500" />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Orden de aparición</label>
              <input v-model.number="form.orden" type="number" class="form-control" />
            </div>
            <div class="col-md-4 d-flex align-items-end">
              <div class="form-check pb-2">
                <input v-model="form.destacado" type="checkbox" class="form-check-input" id="eventoDestacado" />
                <label class="form-check-label fw-semibold" for="eventoDestacado">Destacado en portada</label>
              </div>
            </div>
            <div class="col-md-4 d-flex align-items-end">
              <div class="form-check pb-2">
                <input v-model="form.publicado" type="checkbox" class="form-check-input" id="eventoPublicado" />
                <label class="form-check-label fw-semibold" for="eventoPublicado">Visible en el sitio</label>
              </div>
            </div>

            <div class="col-12">
              <label class="form-label fw-semibold">Imagen destacada</label>
              <div v-if="!editandoId" class="text-secondary small p-2 rounded bg-dark bg-opacity-25">
                ℹ Guarda los datos del evento primero para habilitar la carga de la imagen principal.
              </div>
              <ImagenUpload v-else :imagen-url="eventoActual()?.imagen_url ?? null"
                @subir="subirImagen" @quitar="quitarImagen" />
            </div>

            <div v-if="editandoId" class="col-12">
              <label class="form-label fw-semibold">Galería de Fotos <span class="text-secondary fw-normal">({{ fotos.length }} fotos)</span></label>
              <div v-if="fotos.length" class="d-flex flex-wrap gap-3 mb-2">
                <div v-for="f in fotos" :key="f.id" class="position-relative">
                  <div class="card-cover rounded" style="height: 6rem; width: 6rem"
                    :style="f.imagen_url ? { backgroundImage: `url('${f.imagen_url}')` } : {}"></div>
                  <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0 py-0 px-1"
                    title="Eliminar foto" @click="eliminarFoto(f)">×</button>
                </div>
              </div>
              <div v-else class="text-secondary small mb-2">Sin fotos en la galería todavía.</div>
              <input type="file" multiple accept="image/png,image/jpeg,image/webp,image/gif"
                class="form-control form-control-sm" :disabled="subiendoFoto" @change="agregarFoto" />
              <div class="form-text">
                {{ subiendoFoto ? 'Subiendo fotos...' : 'Puedes seleccionar varias fotos a la vez.' }}
              </div>
            </div>

            <div v-if="error" class="col-12"><div class="alert alert-danger py-2 mb-0">{{ error }}</div></div>
          </form>
        </div>
        <div class="modal-footer border-top border-secondary border-opacity-25 d-flex justify-content-between">
          <div class="d-flex align-items-center gap-2">
            <span v-if="guardadoOk" class="text-success small fw-bold">✓ Cambios guardados correctamente</span>
          </div>
          <div class="d-flex gap-2">
            <button type="button" class="btn btn-outline-secondary" @click="cancelar">Cancelar</button>
            <button type="submit" form="formEventoModal" class="btn btn-orion" :disabled="guardando">
              {{ guardando ? 'Guardando...' : 'Guardar Evento' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- VISTA 1: EN TARJETAS (CARDS) -->
  <div v-if="vista === 'cards'" class="row g-3">
    <div v-for="ev in filtrados" :key="ev.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card admin-card-clickable hover-scale" @click="editar(ev)">
        <div class="admin-thumb" :style="ev.imagen_url ? { backgroundImage: `url('${ev.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ ev.nombre }}</h6>
          <div class="small text-secondary mb-2">{{ ev.cliente }} · {{ ev.fecha_realizacion }}</div>
          <div class="d-flex gap-1 flex-wrap">
            <span class="admin-badge-estado" :class="ev.publicado ? 'text-success' : 'text-secondary'">
              {{ ev.publicado ? 'Visible' : 'Oculto' }}
            </span>
            <span v-if="ev.destacado" class="admin-badge-estado text-orion-primary">Destacado</span>
          </div>
        </div>
        <div class="card-footer bg-transparent d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary btn-sm" @click.stop="editar(ev)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(ev)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!eventos.length" class="col-12 text-secondary">Sin eventos todavía. Crea el primero con “+ Nuevo evento”.</div>
    <div v-else-if="!filtrados.length" class="col-12 text-secondary">Ningún evento coincide con “{{ busqueda }}”.</div>
  </div>

  <!-- VISTA 2: EN LISTA (TABLA) -->
  <div v-else class="card admin-card overflow-hidden">
    <div class="table-responsive mb-0">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-dark">
          <tr>
            <th style="width: 60px;">Imagen</th>
            <th>Nombre del Evento</th>
            <th>Cliente & Fecha</th>
            <th>Tipo</th>
            <th style="width: 90px;">Destacado</th>
            <th style="width: 100px;">Estado</th>
            <th style="width: 150px;" class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ev in filtrados" :key="ev.id" class="admin-card-clickable" @click="editar(ev)">
            <td>
              <img
                v-if="ev.imagen_url"
                :src="ev.imagen_url"
                :alt="ev.nombre"
                class="rounded"
                style="width: 44px; height: 44px; object-fit: cover;"
              />
              <div v-else class="rounded bg-secondary bg-opacity-25 d-flex align-items-center justify-content-center text-secondary small" style="width: 44px; height: 44px;">
                -
              </div>
            </td>
            <td>
              <div class="fw-semibold">{{ ev.nombre }}</div>
              <small class="text-secondary">{{ ev.lugar }}</small>
            </td>
            <td>
              <div>{{ ev.cliente }}</div>
              <small class="text-secondary">{{ ev.fecha_realizacion }}</small>
            </td>
            <td>
              <span class="badge bg-secondary bg-opacity-25 text-body text-uppercase" style="font-size: 10px;">
                {{ ev.tipo_slug || 'Sin tipo' }}
              </span>
            </td>
            <td>
              <span v-if="ev.destacado" class="badge bg-primary bg-opacity-25 text-primary">★ Sí</span>
              <span v-else class="text-secondary small">No</span>
            </td>
            <td>
              <span class="badge" :class="ev.publicado ? 'bg-success bg-opacity-25 text-success' : 'bg-secondary bg-opacity-25 text-secondary'">
                {{ ev.publicado ? 'Visible' : 'Oculto' }}
              </span>
            </td>
            <td class="text-end">
              <button type="button" class="btn btn-outline-secondary btn-sm me-2" @click.stop="editar(ev)">Editar</button>
              <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(ev)">Eliminar</button>
            </td>
          </tr>
          <tr v-if="!filtrados.length">
            <td colspan="7" class="text-center py-4 text-secondary">
              {{ eventos.length ? `Ningún evento coincide con "${busqueda}".` : 'Sin eventos registrados.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
