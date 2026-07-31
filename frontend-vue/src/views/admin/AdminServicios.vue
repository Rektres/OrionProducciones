<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { adminServiciosService } from '@/services/adminServicios';
import ImagenUpload from '@/components/admin/ImagenUpload.vue';
import type { CategoriaServicio, Servicio, ServicioInput } from '@/types';

const servicios = ref<Servicio[]>([]);
const categorias = ref<CategoriaServicio[]>([]);
const mostrarForm = ref(false);
const editandoId = ref<string | null>(null);
const guardando = ref(false);
const error = ref('');

const mostrarCategorias = ref(false);
const nuevaCategoriaNombre = ref('');

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
};

const cancelar = () => {
  mostrarForm.value = false;
  editandoId.value = null;
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
  try {
    if (editandoId.value) {
      await adminServiciosService.actualizar(editandoId.value, form);
    } else {
      const creado = await adminServiciosService.crear(form);
      editandoId.value = creado.id;
    }
    await cargar();
  } catch (e) {
    error.value = aplanarError(e);
  } finally {
    guardando.value = false;
  }
};

const eliminar = async (s: Servicio) => {
  if (!confirm(`¿Eliminar el servicio "${s.nombre}"?`)) return;
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
  texto.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const agregarCategoria = async () => {
  const nombre = nuevaCategoriaNombre.value.trim();
  if (!nombre) return;
  await adminServiciosService.crearCategoria(nombre, slugify(nombre));
  nuevaCategoriaNombre.value = '';
  categorias.value = await adminServiciosService.listarCategorias();
};

const eliminarCategoria = async (c: CategoriaServicio) => {
  if (!confirm(`¿Eliminar la categoría "${c.nombre}"? Los servicios que la usen quedarán sin categoría.`)) return;
  await adminServiciosService.eliminarCategoria(c.id);
  await cargar();
};
</script>

<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h4 class="mb-0">Servicios</h4>
    <button type="button" class="btn btn-orion btn-sm" @click="nuevo">Nuevo servicio</button>
  </div>

  <div class="card admin-card p-3 mb-4">
    <div class="d-flex justify-content-between align-items-center" style="cursor: pointer" @click="mostrarCategorias = !mostrarCategorias">
      <h6 class="mb-0">Categorías</h6>
      <span class="text-secondary">{{ mostrarCategorias ? '▲' : '▼' }}</span>
    </div>
    <div v-if="mostrarCategorias" class="mt-3">
      <ul class="list-group list-group-flush mb-2">
        <li v-for="c in categorias" :key="c.id"
          class="list-group-item admin-card text-white d-flex justify-content-between align-items-center px-0">
          {{ c.nombre }}
          <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminarCategoria(c)">Eliminar</button>
        </li>
        <li v-if="!categorias.length" class="list-group-item admin-card text-secondary px-0">Sin categorías todavía.</li>
      </ul>
      <div class="input-group input-group-sm">
        <input v-model="nuevaCategoriaNombre" type="text" class="form-control" placeholder="Nueva categoría..."
          @keyup.enter="agregarCategoria" />
        <button type="button" class="btn btn-outline-light" @click="agregarCategoria">Agregar</button>
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
        <label class="form-label">Categoría</label>
        <select v-model="form.categoria" class="form-select">
          <option :value="null">Sin categoría</option>
          <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
        </select>
      </div>
      <div class="col-12">
        <label class="form-label">Descripción corta *</label>
        <textarea v-model="form.descripcion_corta" required rows="2" class="form-control"></textarea>
      </div>
      <div class="col-12">
        <label class="form-label">Descripción larga *</label>
        <textarea v-model="form.descripcion_larga" required rows="4" class="form-control"></textarea>
      </div>
      <div class="col-12">
        <label class="form-label">Ícono (SVG)</label>
        <textarea v-model="form.icono_svg" rows="2" class="form-control"></textarea>
      </div>
      <div class="col-md-3">
        <label class="form-label">Orden</label>
        <input v-model.number="form.orden" type="number" class="form-control" />
      </div>
      <div class="col-md-3 d-flex align-items-end">
        <div class="form-check">
          <input v-model="form.activo" type="checkbox" class="form-check-input" id="servicioActivo" />
          <label class="form-check-label" for="servicioActivo">Activo</label>
        </div>
      </div>
      <div class="col-12">
        <label class="form-label">Imagen</label>
        <div v-if="!editandoId" class="text-secondary small">Guarda el servicio primero para poder subir una imagen.</div>
        <ImagenUpload v-else :imagen-url="servicioActual()?.imagen_url ?? null"
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
    <div v-for="s in servicios" :key="s.id" class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card h-100 admin-card hover-scale" role="button" @click="editar(s)">
        <div class="card-cover rounded-top" style="height: 8rem"
          :style="s.imagen_url ? { backgroundImage: `url('${s.imagen_url}')` } : {}"></div>
        <div class="card-body">
          <h6 class="card-title mb-1">{{ s.nombre }}</h6>
          <div class="small text-secondary">{{ s.categoria_slug || 'sin categoría' }} · {{ s.activo ? 'Activo' : 'Inactivo' }}</div>
        </div>
        <div class="card-footer admin-card d-flex justify-content-between">
          <button type="button" class="btn btn-outline-light btn-sm" @click.stop="editar(s)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click.stop="eliminar(s)">Eliminar</button>
        </div>
      </div>
    </div>
    <div v-if="!servicios.length" class="col-12 text-secondary">Sin servicios todavía.</div>
  </div>
</template>
