<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { adminServiciosService } from '@/services/adminServicios';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { CategoriaServicio, Servicio, ServicioInput } from '@/types';

const servicios = ref<Servicio[]>([]);
const categorias = ref<CategoriaServicio[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');
const guardadoOk = ref(false);
const busqueda = ref('');
const vista = ref<'cards' | 'lista'>('cards');

const mostrarCategorias = ref(false);
const nuevaCategoriaNombre = ref('');

const filtrados = computed(() => {
  const q = busqueda.value.trim().toLowerCase();
  if (!q) return servicios.value;
  return servicios.value.filter((s) =>
    s.nombre.toLowerCase().includes(q) || (s.categoria_slug || '').toLowerCase().includes(q));
});

const formVacio = (): ServicioInput => ({
  nombre: '',
  categoria: null,
  descripcion_corta: '',
  descripcion_larga: '',
  icono_svg: '',
  activo: true,
  orden: 0,
});

const form = reactive<ServicioInput>(formVacio());

const cargar = async () => {
  [categorias.value, servicios.value] = await Promise.all([
    adminServiciosService.listarCategorias(),
    adminServiciosService.listar(),
  ]);
};

onMounted(cargar);

const nuevo = () => {
  Object.assign(form, formVacio());
  editandoId.value = null;
  mostrarForm.value = true;
  error.value = '';
  guardadoOk.value = false;
};

const editar = (s: Servicio) => {
  Object.assign(form, {
    nombre: s.nombre,
    categoria: s.categoria,
    descripcion_corta: s.descripcion_corta,
    descripcion_larga: s.descripcion_larga,
    icono_svg: s.icono_svg || '',
    activo: s.activo,
    orden: s.orden,
  });
  editandoId.value = s.id;
  mostrarForm.value = true;
  error.value = '';
  guardadoOk.value = false;
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
  guardadoOk.value = false;
};

const aplanarError = (e: any): string => {
  const data = e?.response?.data;
  if (!data) return 'Error guardando el servicio.';
  if (typeof data === 'string') return data;
  return Object.values(data).flat().join(' ');
};

const guardar = async () => {
  guardando.value = true;
  error.value = '';
  guardadoOk.value = false;
  try {
    if (editandoId.value) {
      await adminServiciosService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminServiciosService.crear(form);
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

const eliminar = async (s: Servicio) => {
  if (!confirm(`¿Eliminar el servicio "${s.nombre}"?\n\nEsta acción no se puede deshacer.`)) return;
  await adminServiciosService.eliminar(s.id);
  if (editandoId.value === s.id) cancelar();
  await cargar();
};

const subirImagen = async (archivo: File) => {
  if (!editandoId.value) return;
  await adminServiciosService.subirImagen(editandoId.value, archivo);
  await cargar();
};

const quitarImagen = async () => {
  if (!editandoId.value) return;
  await adminServiciosService.quitarImagen(editandoId.value);
  await cargar();
};

const servicioActual = () => servicios.value.find((s) => s.id === editandoId.value) || null;

const slugify = (texto: string) =>
  texto.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const agregarCategoria = async () => {
  const nombre = nuevaCategoriaNombre.value.trim();
  if (!nombre) return;
  await adminServiciosService.crearCategoria(nombre, slugify(nombre));
  nuevaCategoriaNombre.value = '';
  categorias.value = await adminServiciosService.listarCategorias();
};

const eliminarCategoria = async (c: CategoriaServicio) => {
  if (!confirm(`¿Eliminar la categoría "${c.nombre}"?\n\nLos servicios que la usen quedarán sin categoría.`)) return;
  await adminServiciosService.eliminarCategoria(c.id);
  await cargar();
};
</script>

<template>
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
    <div>
      <h4 class="mb-0">Servicios</h4>
      <small class="text-secondary">{{ servicios.length }} en total</small>
    </div>
    <div class="d-flex gap-2 flex-wrap align-items-center">
      <input v-model="busqueda" type="search" class="form-control form-control-sm admin-toolbar-search"
        placeholder="Buscar por nombre o categoría..." />
      
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

      <button type="button" class="btn btn-orion btn-sm" @click="nuevo">+ Nuevo servicio</button>
    </div>
  </div>

  <div class="card admin-card p-3 mb-4">
    <div class="d-flex justify-content-between align-items-center admin-card-clickable"
      @click="mostrarCategorias = !mostrarCategorias">
      <h6 class="mb-0">Categorías <span class="text-secondary fw-normal">({{ categorias.length }})</span></h6>
      <span class="text-secondary">{{ mostrarCategorias ? '▲' : '▼' }}</span>
    </div>
    <div v-if="mostrarCategorias" class="mt-3">
      <ul class="list-group list-group-flush mb-2">
        <li v-for="c in categorias" :key="c.id"
          class="list-group-item d-flex justify-content-between align-items-center px-0">
          {{ c.nombre }}
          <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminarCategoria(c)">Eliminar</button>
        </li>
        <li v-if="!categorias.length" class="list-group-item text-secondary px-0">Sin categorías todavía.</li>
      </ul>
      <div class="input-group input-group-sm">
        <input v-model="nuevaCategoriaNombre" type="text" class="form-control" placeholder="Nueva categoría..."
          @keyup.enter="agregarCategoria" />
        <button type="button" class="btn btn-outline-secondary" @click="agregarCategoria">Agregar</button>
      </div>
    </div>
  </div>

  <!-- MODAL DE CREACIÓN / EDICIÓN DE SERVICIO -->
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
          <h5 class="modal-title mb-0">{{ editandoId ? 'Editar servicio' : 'Nuevo servicio' }}</h5>
          <button type="button" class="btn-close" aria-label="Cerrar" @click="cancelar"></button>
        </div>
        <div class="modal-body p-4">
          <form id="formServicioModal" class="row g-3" @submit.prevent="guardar">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Nombre *</label>
              <input v-model="form.nombre" type="text" required class="form-control" placeholder="Ej: Iluminación Robótica & Láser" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Categoría</label>
              <select v-model="form.categoria" class="form-select">
                <option :value="null">Sin categoría</option>
                <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Descripción corta *</label>
              <textarea v-model="form.descripcion_corta" required rows="2" class="form-control" placeholder="Resumen breve para tarjetas y modales públicos..."></textarea>
              <div class="form-text">Es la que se muestra en el modal del sitio público.</div>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Descripción larga *</label>
              <textarea v-model="form.descripcion_larga" required rows="4" class="form-control" placeholder="Detalle técnico completo y equipamiento incluido..."></textarea>
            </div>
            <div class="col-md-4">
              <label class="form-label fw-semibold">Orden de aparición</label>
              <input v-model.number="form.orden" type="number" class="form-control" />
            </div>
            <div class="col-md-4 d-flex align-items-end">
              <div class="form-check pb-2">
                <input v-model="form.activo" type="checkbox" class="form-check-input" id="servicioActivo" />
                <label class="form-check-label fw-semibold" for="servicioActivo">Visible en el sitio</label>
              </div>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold">Ícono (SVG inline opcional)</label>
              <textarea v-model="form.icono_svg" rows="2" class="form-control" placeholder="<svg ...>...</svg>"></textarea>
            </div>

            <div class="col-12">
              <label class="form-label fw-semibold">Imagen</label>
              <div v-if="!editandoId" class="text-secondary small p-2 rounded bg-dark bg-opacity-25">
                ℹ Guarda los datos del servicio primero para habilitar la carga de imagen.
              </div>
              <ImagenUpload v-else :imagen-url="servicioActual()?.imagen_url ?? null"
                @subir="subirImagen" @quitar="quitarImagen" />
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
            <button type="submit" form="formServicioModal" class="btn btn-orion" :disabled="guardando">
              {{ guardando ? 'Guardando...' : 'Guardar Servicio' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- VISTA 1: EN TARJETAS (CARDS) -->
  <div v-if="vista === 'cards'" class="row g-3">
    <div v-for="s in filtrados" :key="s.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card admin-card-clickable hover-scale" @click="editar(s)">
        <div class="admin-thumb" :style="s.imagen_url ? { backgroundImage: `url('${s.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ s.nombre }}</h6>
          <div class="small text-secondary mb-2">{{ s.categoria_slug || 'sin categoría' }}</div>
          <span class="badge" :class="s.activo ? 'badge-estado-visible' : 'badge-estado-oculto'">
            {{ s.activo ? '● Visible' : 'Oculto' }}
          </span>
        </div>
        <div class="card-footer bg-transparent d-flex justify-content-between">
          <button type="button" class="btn btn-outline-secondary btn-sm" @click.stop="editar(s)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(s)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!servicios.length" class="col-12 text-secondary">Sin servicios todavía. Crea el primero con “+ Nuevo servicio”.</div>
    <div v-else-if="!filtrados.length" class="col-12 text-secondary">Ningún servicio coincide con “{{ busqueda }}”.</div>
  </div>

  <!-- VISTA 2: EN LISTA (TABLA) -->
  <div v-else class="card admin-card overflow-hidden">
    <div class="table-responsive mb-0">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-dark">
          <tr>
            <th style="width: 60px;">Imagen</th>
            <th>Nombre del Servicio</th>
            <th>Categoría</th>
            <th style="width: 100px;">Orden</th>
            <th style="width: 110px;">Estado</th>
            <th style="width: 150px;" class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in filtrados" :key="s.id" class="admin-card-clickable" @click="editar(s)">
            <td>
              <img
                v-if="s.imagen_url"
                :src="s.imagen_url"
                :alt="s.nombre"
                class="rounded"
                style="width: 44px; height: 44px; object-fit: cover;"
              />
              <div v-else class="bg-secondary bg-opacity-25 rounded d-flex align-items-center justify-content-center text-secondary small" style="width: 44px; height: 44px;">
                -
              </div>
            </td>
            <td>
              <div class="fw-semibold">{{ s.nombre }}</div>
              <small class="text-secondary text-truncate d-block" style="max-width: 320px;">{{ s.descripcion_corta }}</small>
            </td>
            <td>
              <span class="badge badge-categoria text-uppercase" style="font-size: 10px;">
                {{ s.categoria_slug || 'Sin categoría' }}
              </span>
            </td>
            <td>{{ s.orden }}</td>
            <td>
              <span class="badge" :class="s.activo ? 'badge-estado-visible' : 'badge-estado-oculto'">
                {{ s.activo ? '● Visible' : 'Oculto' }}
              </span>
            </td>
            <td class="text-end">
              <button type="button" class="btn btn-outline-secondary btn-sm me-2" @click.stop="editar(s)">Editar</button>
              <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(s)">Eliminar</button>
            </td>
          </tr>
          <tr v-if="!filtrados.length">
            <td colspan="6" class="text-center py-4 text-secondary">
              {{ servicios.length ? `Ningún servicio coincide con "${busqueda}".` : 'Sin servicios registrados.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
