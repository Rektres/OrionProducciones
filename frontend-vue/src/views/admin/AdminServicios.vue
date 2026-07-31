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
</script>

<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h4 class="mb-0">Servicios</h4>
    <button type="button" class="btn btn-orion btn-sm" @click="nuevo">Nuevo servicio</button>
  </div>

  <div v-if="mostrarForm" class="card bg-dark border-secondary p-3 mb-4">
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

  <table class="table table-dark table-sm align-middle">
    <thead>
      <tr>
        <th></th>
        <th>Nombre</th>
        <th>Categoría</th>
        <th>Activo</th>
        <th>Orden</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="s in servicios" :key="s.id">
        <td style="width: 60px">
          <div v-if="s.imagen_url" class="card-cover rounded" style="height: 2.5rem; width: 2.5rem"
            :style="{ backgroundImage: `url('${s.imagen_url}')` }"></div>
        </td>
        <td>{{ s.nombre }}</td>
        <td>{{ s.categoria_slug || '-' }}</td>
        <td>{{ s.activo ? 'Sí' : 'No' }}</td>
        <td>{{ s.orden }}</td>
        <td class="text-end">
          <button type="button" class="btn btn-outline-light btn-sm me-2" @click="editar(s)">Editar</button>
          <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminar(s)">Eliminar</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
