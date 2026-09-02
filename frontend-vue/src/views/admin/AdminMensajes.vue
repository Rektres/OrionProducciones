<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { adminCotizacionesService } from '@/services/adminCotizaciones';
import type { Cotizacion, EstadoCotizacion, ResponderCotizacionInput } from '@/types';

const cotizaciones = ref<Cotizacion[]>([]);
const cargando = ref(false);
const busqueda = ref('');
const filtroEstado = ref<string>('todos');
const vista = ref<'lista' | 'cards'>('lista');

// Modal de detalle y respuesta
const modalAbierto = ref(false);
const cotizacionSeleccionada = ref<Cotizacion | null>(null);
const pestanaModal = ref<'detalle' | 'responder'>('detalle');

// Estado de respuesta de correo
const enviandoRespuesta = ref(false);
const errorRespuesta = ref('');
const respuestaExitosa = ref('');
const formRespuesta = reactive<ResponderCotizacionInput>({
  asunto: '',
  mensaje: '',
  nuevo_estado: 'en_contacto',
});

// Plantillas de respuesta rápida
const plantillas = [
  {
    titulo: '1. Propuesta en preparación',
    asunto: 'Propuesta técnica y cotización en preparación — Orion Stage',
    texto: (_nombre: string, tipo: string) =>
      `Muchas gracias por contactar a Orion Stage.\n\n` +
      `Te confirmamos que nuestro equipo de producción ejecutiva se encuentra evaluando los requerimientos de tu evento (${tipo}) ` +
      `para diseñar una propuesta técnica integral y a la medida.\n\n` +
      `En breve te compartiremos la propuesta detallada con equipamiento, montaje y valores referenciales.\n\n` +
      `Si deseas afinar algún requerimiento adicional o coordinar una llamada, quedamos a tu entera disposición.`,
    estado: 'en_contacto' as EstadoCotizacion,
  },
  {
    titulo: '2. Coordinar reunión / llamada',
    asunto: 'Coordinemos una breve llamada para tu evento — Orion Stage',
    texto: (_nombre: string, tipo: string) =>
      `Qué gusto saludarte.\n\n` +
      `Hemos revisado con entusiasmo tu solicitud para el evento (${tipo}). Para afinar los aspectos técnicos de audio, iluminación, escenario y logística con precisión, ` +
      `nos encantaría agendar una breve llamada de 10 minutos o coordinar vía WhatsApp según tu preferencia.\n\n` +
      `¿Qué día y horario te acomoda mejor para conversar?`,
    estado: 'en_contacto' as EstadoCotizacion,
  },
  {
    titulo: '3. Cotización lista para revisión',
    asunto: 'Cotización disponible para tu evento — Orion Stage',
    texto: (_nombre: string, tipo: string) =>
      `Te saludamos cordialmente del equipo de Orion Stage.\n\n` +
      `Te confirmamos que ya hemos preparado la cotización y propuesta técnica para tu evento (${tipo}). ` +
      `A continuación te compartimos los detalles para tu revisión y estamos atentos a cualquier consulta o ajuste que requieras.\n\n` +
      `¡Quedamos muy atentos para hacer de tu evento una experiencia inolvidable!`,
    estado: 'cotizado' as EstadoCotizacion,
  },
];

const cargarCotizaciones = async () => {
  cargando.value = true;
  try {
    cotizaciones.value = await adminCotizacionesService.listar();
  } catch (err) {
    console.error('Error cargando cotizaciones:', err);
  } finally {
    cargando.value = false;
  }
};

onMounted(cargarCotizaciones);

// Estadísticas para contadores
const totalNuevos = computed(() => cotizaciones.value.filter((c) => c.estado === 'nuevo').length);
const totalEnContacto = computed(() => cotizaciones.value.filter((c) => c.estado === 'en_contacto').length);
const totalCotizados = computed(() => cotizaciones.value.filter((c) => c.estado === 'cotizado').length);
const totalCerrados = computed(() => cotizaciones.value.filter((c) => c.estado === 'cerrado').length);
const totalDescartados = computed(() => cotizaciones.value.filter((c) => c.estado === 'descartado').length);

// Filtrado reactivo por texto y estado
const filtradas = computed(() => {
  let list = cotizaciones.value;

  if (filtroEstado.value !== 'todos') {
    list = list.filter((c) => c.estado === filtroEstado.value);
  }

  const q = busqueda.value.trim().toLowerCase();
  if (q) {
    list = list.filter(
      (c) =>
        c.nombre.toLowerCase().includes(q) ||
        c.email.toLowerCase().includes(q) ||
        (c.empresa && c.empresa.toLowerCase().includes(q)) ||
        c.tipo_evento.toLowerCase().includes(q) ||
        c.descripcion.toLowerCase().includes(q)
    );
  }

  return list;
});

const abrirDetalle = (c: Cotizacion, tab: 'detalle' | 'responder' = 'detalle') => {
  cotizacionSeleccionada.value = { ...c };
  pestanaModal.value = tab;
  errorRespuesta.value = '';
  respuestaExitosa.value = '';

  // Inicializar asunto y estado por defecto
  formRespuesta.asunto = `Respuesta a tu cotización para ${c.tipo_evento} — Orion Stage`;
  formRespuesta.mensaje = `Hola ${c.nombre},\n\nMuchas gracias por escribirnos a Orion Stage respecto a tu requerimiento.\n\n`;
  formRespuesta.nuevo_estado = c.estado === 'nuevo' ? 'en_contacto' : c.estado;

  modalAbierto.value = true;
};

const cerrarModal = () => {
  modalAbierto.value = false;
  cotizacionSeleccionada.value = null;
  errorRespuesta.value = '';
  respuestaExitosa.value = '';
};

const aplicarPlantilla = (p: typeof plantillas[0]) => {
  if (!cotizacionSeleccionada.value) return;
  const c = cotizacionSeleccionada.value;
  formRespuesta.asunto = p.asunto;
  formRespuesta.mensaje = `Hola ${c.nombre},\n\n` + p.texto(c.nombre, c.tipo_evento);
  formRespuesta.nuevo_estado = p.estado;
};

const cambiarEstado = async (nuevoEstado: EstadoCotizacion) => {
  if (!cotizacionSeleccionada.value) return;
  try {
    const actualizada = await adminCotizacionesService.actualizarEstado(
      cotizacionSeleccionada.value.id,
      nuevoEstado
    );
    cotizacionSeleccionada.value.estado = actualizada.estado;
    const idx = cotizaciones.value.findIndex((c) => c.id === actualizada.id);
    if (idx !== -1) cotizaciones.value[idx].estado = actualizada.estado;
  } catch (err) {
    console.error('Error actualizando estado:', err);
    alert('No se pudo actualizar el estado.');
  }
};

const enviarRespuesta = async () => {
  if (!cotizacionSeleccionada.value) return;
  if (!formRespuesta.asunto.trim() || !formRespuesta.mensaje.trim()) {
    errorRespuesta.value = 'Por favor completa el asunto y el mensaje antes de enviar.';
    return;
  }

  enviandoRespuesta.value = true;
  errorRespuesta.value = '';
  respuestaExitosa.value = '';

  try {
    const res = await adminCotizacionesService.responder(
      cotizacionSeleccionada.value.id,
      formRespuesta
    );
    respuestaExitosa.value = res.mensaje || '¡Correo enviado con éxito!';
    cotizacionSeleccionada.value.estado = res.cotizacion.estado;

    // Actualizar en listado general
    const idx = cotizaciones.value.findIndex((c) => c.id === res.cotizacion.id);
    if (idx !== -1) cotizaciones.value[idx] = res.cotizacion;

    setTimeout(() => {
      pestanaModal.value = 'detalle';
    }, 1800);
  } catch (err: any) {
    errorRespuesta.value =
      err?.response?.data?.error || 'Ocurrió un error al enviar el correo. Revisa la configuración SMTP.';
  } finally {
    enviandoRespuesta.value = false;
  }
};

const eliminarCotizacion = async (c: Cotizacion) => {
  if (!confirm(`¿Eliminar la cotización de "${c.nombre}"?\nEsta acción no se puede deshacer.`)) return;
  try {
    await adminCotizacionesService.eliminar(c.id);
    cotizaciones.value = cotizaciones.value.filter((item) => item.id !== c.id);
    if (cotizacionSeleccionada.value?.id === c.id) cerrarModal();
  } catch (err) {
    console.error('Error eliminando cotización:', err);
    alert('No se pudo eliminar la cotización.');
  }
};

// Formateadores visuales
const formatearFecha = (fechaIso: string) => {
  if (!fechaIso) return '-';
  try {
    const d = new Date(fechaIso);
    return d.toLocaleDateString('es-CL', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return fechaIso;
  }
};

const badgeClaseEstado = (estado: EstadoCotizacion) => {
  switch (estado) {
    case 'nuevo':
      return 'bg-warning text-dark fw-bold';
    case 'en_contacto':
      return 'bg-info bg-opacity-25 text-info border border-info border-opacity-50';
    case 'cotizado':
      return 'bg-primary bg-opacity-25 text-primary border border-primary border-opacity-50';
    case 'cerrado':
      return 'bg-success bg-opacity-25 text-success border border-success border-opacity-50';
    case 'descartado':
      return 'bg-secondary bg-opacity-25 text-secondary';
    default:
      return 'bg-secondary';
  }
};

const labelEstado = (estado: EstadoCotizacion) => {
  switch (estado) {
    case 'nuevo':
      return '● Nuevo';
    case 'en_contacto':
      return 'En contacto';
    case 'cotizado':
      return 'Cotizado';
    case 'cerrado':
      return '✓ Cerrado';
    case 'descartado':
      return 'Descartado';
    default:
      return estado;
  }
};

const obtenerLinkWhatsapp = (c: Cotizacion) => {
  if (!c.telefono) return '#';
  const cleanPhone = c.telefono.replace(/[^0-9]/g, '');
  const msg = encodeURIComponent(
    `Hola ${c.nombre}, te contactamos desde Orion Stage respecto a tu cotización para ${c.tipo_evento}.`
  );
  return `https://wa.me/${cleanPhone}?text=${msg}`;
};
</script>

<template>
  <div class="admin-mensajes-container">
    <!-- ENCABEZADO Y CONTADORES -->
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
      <div>
        <h4 class="mb-1 text-orion-gold fw-bold">Bandeja de Mensajes y Cotizaciones</h4>
        <p class="text-secondary small mb-0">
          Gestiona las consultas recibidas desde la web, actualiza prospectos y responde oficialmente por correo y WhatsApp.
        </p>
      </div>

      <div class="d-flex gap-2 align-items-center">
        <button
          type="button"
          class="btn btn-outline-secondary btn-sm"
          title="Actualizar listado"
          :disabled="cargando"
          @click="cargarCotizaciones"
        >
          <span v-if="cargando" class="spinner-border spinner-border-sm me-1" role="status"></span>
          🔄 Recargar
        </button>
      </div>
    </div>

    <!-- TARJETAS DE RESUMEN (STATS) -->
    <div class="row g-2 mb-4">
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-primary shadow-sm': filtroEstado === 'todos' }"
          @click="filtroEstado = 'todos'"
        >
          <small class="text-secondary d-block text-uppercase" style="font-size: 11px;">Total</small>
          <span class="fs-4 fw-bold">{{ cotizaciones.length }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-warning shadow-sm': filtroEstado === 'nuevo' }"
          @click="filtroEstado = 'nuevo'"
        >
          <small class="text-warning d-block text-uppercase" style="font-size: 11px;">● Nuevos</small>
          <span class="fs-4 fw-bold text-warning">{{ totalNuevos }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-info shadow-sm': filtroEstado === 'en_contacto' }"
          @click="filtroEstado = 'en_contacto'"
        >
          <small class="text-info d-block text-uppercase" style="font-size: 11px;">En contacto</small>
          <span class="fs-4 fw-bold text-info">{{ totalEnContacto }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-primary shadow-sm': filtroEstado === 'cotizado' }"
          @click="filtroEstado = 'cotizado'"
        >
          <small class="text-primary d-block text-uppercase" style="font-size: 11px;">Cotizados</small>
          <span class="fs-4 fw-bold text-primary">{{ totalCotizados }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-success shadow-sm': filtroEstado === 'cerrado' }"
          @click="filtroEstado = 'cerrado'"
        >
          <small class="text-success d-block text-uppercase" style="font-size: 11px;">✓ Cerrados</small>
          <span class="fs-4 fw-bold text-success">{{ totalCerrados }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-secondary shadow-sm': filtroEstado === 'descartado' }"
          @click="filtroEstado = 'descartado'"
        >
          <small class="text-secondary d-block text-uppercase" style="font-size: 11px;">Descartados</small>
          <span class="fs-4 fw-bold text-secondary">{{ totalDescartados }}</span>
        </div>
      </div>
    </div>

    <!-- TOOLBAR DE BÚSQUEDA Y VISTAS -->
    <div class="card admin-card p-3 mb-4">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
        <!-- Buscador -->
        <div class="flex-grow-1" style="max-width: 400px;">
          <input
            v-model="busqueda"
            type="search"
            class="form-control form-control-sm admin-toolbar-search"
            placeholder="Buscar por cliente, email, empresa o requerimiento..."
          />
        </div>

        <!-- Filtros Chips -->
        <div class="d-flex gap-1 flex-wrap align-items-center">
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'todos' ? 'btn-orion' : 'btn-outline-secondary'"
            @click="filtroEstado = 'todos'"
          >
            Todos
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'nuevo' ? 'btn-warning text-dark fw-bold' : 'btn-outline-secondary'"
            @click="filtroEstado = 'nuevo'"
          >
            Nuevos ({{ totalNuevos }})
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'en_contacto' ? 'btn-info text-dark fw-bold' : 'btn-outline-secondary'"
            @click="filtroEstado = 'en_contacto'"
          >
            En contacto
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'cotizado' ? 'btn-primary' : 'btn-outline-secondary'"
            @click="filtroEstado = 'cotizado'"
          >
            Cotizados
          </button>
        </div>

        <!-- Selector de Vista Cards / Lista -->
        <div class="btn-group btn-group-sm" role="group" aria-label="Cambiar vista">
          <button
            type="button"
            class="btn"
            :class="vista === 'lista' ? 'btn-primary' : 'btn-outline-secondary'"
            title="Vista en lista"
            @click="vista = 'lista'"
          >
            ☰ Lista
          </button>
          <button
            type="button"
            class="btn"
            :class="vista === 'cards' ? 'btn-primary' : 'btn-outline-secondary'"
            title="Vista en tarjetas"
            @click="vista = 'cards'"
          >
            ⊞ Tarjetas
          </button>
        </div>
      </div>
    </div>

    <!-- LISTADO - VISTA 1: TABLA (LISTA) -->
    <div v-if="vista === 'lista'" class="card admin-card overflow-hidden shadow-sm">
      <div class="table-responsive mb-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-dark">
            <tr>
              <th style="width: 120px;">Estado</th>
              <th style="width: 160px;">Fecha / Hora</th>
              <th>Cliente / Empresa</th>
              <th>Tipo de Evento</th>
              <th>Fecha Est.</th>
              <th>Presupuesto</th>
              <th style="width: 200px;" class="text-end">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in filtradas"
              :key="c.id"
              class="admin-card-clickable"
              @click="abrirDetalle(c, 'detalle')"
            >
              <td>
                <span class="badge py-1 px-2" :class="badgeClaseEstado(c.estado)">
                  {{ labelEstado(c.estado) }}
                </span>
              </td>
              <td>
                <small class="text-secondary">{{ formatearFecha(c.created_at) }}</small>
              </td>
              <td>
                <div class="fw-bold">{{ c.nombre }}</div>
                <div class="small text-secondary">
                  <span>{{ c.email }}</span>
                  <span v-if="c.empresa"> · {{ c.empresa }}</span>
                </div>
              </td>
              <td>
                <span class="badge bg-secondary bg-opacity-25 text-body text-uppercase" style="font-size: 11px;">
                  {{ c.tipo_evento }}
                </span>
              </td>
              <td>
                <small>{{ c.fecha_estimada || 'Por definir' }}</small>
              </td>
              <td>
                <span v-if="c.presupuesto_estimado" class="text-success small fw-semibold">
                  {{ c.presupuesto_estimado }}
                </span>
                <span v-else class="text-secondary small">-</span>
              </td>
              <td class="text-end">
                <button
                  type="button"
                  class="btn btn-outline-primary btn-sm me-1"
                  title="Ver detalle"
                  @click.stop="abrirDetalle(c, 'detalle')"
                >
                  👁 Ver
                </button>
                <button
                  type="button"
                  class="btn btn-orion btn-sm me-1"
                  title="Responder por correo"
                  @click.stop="abrirDetalle(c, 'responder')"
                >
                  ✉ Responder
                </button>
                <button
                  type="button"
                  class="btn btn-outline-danger btn-sm"
                  title="Eliminar registro"
                  @click.stop="eliminarCotizacion(c)"
                >
                  ✕
                </button>
              </td>
            </tr>
            <tr v-if="!filtradas.length">
              <td colspan="7" class="text-center py-5 text-secondary">
                {{ cotizaciones.length ? `No hay cotizaciones que coincidan con "${busqueda}".` : 'No se han recibido cotizaciones todavía.' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- LISTADO - VISTA 2: TARJETAS (CARDS) -->
    <div v-else class="row g-3">
      <div v-for="c in filtradas" :key="c.id" class="col-md-6 col-lg-4">
        <div
          class="card h-100 admin-card admin-card-clickable p-3 d-flex flex-column justify-content-between"
          :class="{ 'border-warning': c.estado === 'nuevo' }"
          @click="abrirDetalle(c, 'detalle')"
        >
          <div>
            <div class="d-flex justify-content-between align-items-start mb-2">
              <span class="badge" :class="badgeClaseEstado(c.estado)">
                {{ labelEstado(c.estado) }}
              </span>
              <small class="text-secondary">{{ formatearFecha(c.created_at) }}</small>
            </div>

            <h5 class="card-title mb-1 fw-bold">{{ c.nombre }}</h5>
            <p v-if="c.empresa" class="small text-orion-gold mb-1 fw-semibold">{{ c.empresa }}</p>
            <p class="small text-secondary mb-2">{{ c.email }} {{ c.telefono ? `· ${c.telefono}` : '' }}</p>

            <div class="d-flex gap-2 mb-2">
              <span class="badge bg-secondary bg-opacity-25 text-body text-uppercase" style="font-size: 10px;">
                {{ c.tipo_evento }}
              </span>
              <span v-if="c.fecha_estimada" class="badge bg-dark text-secondary" style="font-size: 10px;">
                📅 {{ c.fecha_estimada }}
              </span>
            </div>

            <p class="small text-body bg-dark bg-opacity-25 p-2 rounded mb-3" style="max-height: 70px; overflow: hidden; text-overflow: ellipsis;">
              "{{ c.descripcion }}"
            </p>
          </div>

          <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-25">
            <a
              v-if="c.telefono"
              :href="obtenerLinkWhatsapp(c)"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-outline-success btn-sm py-1 px-2"
              title="Abrir WhatsApp"
              @click.stop
            >
              WhatsApp
            </a>
            <div class="d-flex gap-1 ms-auto">
              <button
                type="button"
                class="btn btn-orion btn-sm"
                @click.stop="abrirDetalle(c, 'responder')"
              >
                ✉ Responder
              </button>
              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                title="Eliminar"
                @click.stop="eliminarCotizacion(c)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!filtradas.length" class="col-12 text-center py-5 text-secondary">
        {{ cotizaciones.length ? `No hay mensajes que coincidan con "${busqueda}".` : 'No se han recibido mensajes aún.' }}
      </div>
    </div>

    <!-- MODAL DE DETALLE Y GESTIÓN DE RESPUESTA -->
    <div
      v-if="modalAbierto && cotizacionSeleccionada"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.8); z-index: 1060;"
      @click.self="cerrarModal"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
        <div class="modal-content admin-card">
          <!-- CABECERA DEL MODAL -->
          <div class="modal-header border-bottom border-secondary border-opacity-25 pb-3">
            <div>
              <div class="d-flex align-items-center gap-2 mb-1">
                <span class="badge" :class="badgeClaseEstado(cotizacionSeleccionada.estado)">
                  {{ labelEstado(cotizacionSeleccionada.estado) }}
                </span>
                <h5 class="modal-title mb-0 fw-bold">{{ cotizacionSeleccionada.nombre }}</h5>
              </div>
              <small class="text-secondary">
                Recibido el {{ formatearFecha(cotizacionSeleccionada.created_at) }}
              </small>
            </div>
            <button type="button" class="btn-close" aria-label="Cerrar" @click="cerrarModal"></button>
          </div>

          <!-- PESTAÑAS DENTRO DEL MODAL -->
          <div class="px-4 pt-3 border-bottom border-secondary border-opacity-25">
            <ul class="nav nav-tabs border-0">
              <li class="nav-item">
                <button
                  type="button"
                  class="nav-link"
                  :class="{ 'active fw-bold text-orion-gold': pestanaModal === 'detalle' }"
                  @click="pestanaModal = 'detalle'"
                >
                  📋 Detalle del Requerimiento
                </button>
              </li>
              <li class="nav-item">
                <button
                  type="button"
                  class="nav-link"
                  :class="{ 'active fw-bold text-orion-gold': pestanaModal === 'responder' }"
                  @click="pestanaModal = 'responder'"
                >
                  ✉ Redactar Respuesta por Correo
                </button>
              </li>
            </ul>
          </div>

          <!-- CUERPO DEL MODAL -->
          <div class="modal-body p-4">
            <!-- PESTAÑA 1: DETALLE DE COTIZACIÓN -->
            <div v-if="pestanaModal === 'detalle'">
              <!-- Ficha de Datos -->
              <div class="card bg-dark bg-opacity-25 border border-secondary border-opacity-25 p-3 mb-4 rounded">
                <div class="row g-3">
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Correo Electrónico</small>
                    <a :href="`mailto:${cotizacionSeleccionada.email}`" class="text-primary fw-semibold">
                      {{ cotizacionSeleccionada.email }}
                    </a>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Teléfono / WhatsApp</small>
                    <div class="d-flex align-items-center gap-2">
                      <span class="fw-semibold">{{ cotizacionSeleccionada.telefono || 'No especificado' }}</span>
                      <a
                        v-if="cotizacionSeleccionada.telefono"
                        :href="obtenerLinkWhatsapp(cotizacionSeleccionada)"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="badge bg-success text-white text-decoration-none py-1 px-2"
                      >
                        Abrir WhatsApp ↗
                      </a>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Empresa u Organización</small>
                    <span class="fw-semibold">{{ cotizacionSeleccionada.empresa || 'Particular / No indicada' }}</span>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Tipo de Evento</small>
                    <span class="badge bg-secondary text-uppercase">{{ cotizacionSeleccionada.tipo_evento }}</span>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Fecha Estimada</small>
                    <span class="fw-semibold">{{ cotizacionSeleccionada.fecha_estimada || 'Por coordinar' }}</span>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Presupuesto Estimado</small>
                    <span class="fw-bold text-success">{{ cotizacionSeleccionada.presupuesto_estimado || 'A evaluar' }}</span>
                  </div>
                </div>
              </div>

              <!-- Mensaje / Requerimiento -->
              <h6 class="fw-bold mb-2 text-orion-gold">Mensaje o Detalle del Requerimiento:</h6>
              <div class="p-3 bg-dark bg-opacity-50 rounded border-start border-4 border-warning mb-4" style="white-space: pre-wrap; font-size: 14.5px; line-height: 1.6;">
{{ cotizacionSeleccionada.descripcion }}
              </div>

              <!-- Selector Rápido de Estado -->
              <div class="card p-3 bg-dark bg-opacity-25 border border-secondary border-opacity-25">
                <label class="form-label fw-semibold mb-2">Cambiar Estado del Prospecto:</label>
                <div class="d-flex gap-2 flex-wrap">
                  <button
                    v-for="st in (['nuevo', 'en_contacto', 'cotizado', 'cerrado', 'descartado'] as EstadoCotizacion[])"
                    :key="st"
                    type="button"
                    class="btn btn-sm"
                    :class="cotizacionSeleccionada.estado === st ? badgeClaseEstado(st) : 'btn-outline-secondary'"
                    @click="cambiarEstado(st)"
                  >
                    {{ labelEstado(st) }}
                  </button>
                </div>
              </div>
            </div>

            <!-- PESTAÑA 2: REDACTAR RESPUESTA POR CORREO -->
            <div v-else>
              <div class="alert alert-info py-2 px-3 small mb-3">
                ℹ El mensaje será enviado formalmente desde el correo corporativo (SMTP) de Orion Stage a <strong>{{ cotizacionSeleccionada.email }}</strong> con diseño HTML enriquecido.
              </div>

              <!-- Selector de Plantillas Rápidas -->
              <div class="mb-3">
                <label class="form-label small fw-semibold text-secondary">Plantillas de Respuesta Rápida:</label>
                <div class="d-flex gap-2 flex-wrap">
                  <button
                    v-for="(p, idx) in plantillas"
                    :key="idx"
                    type="button"
                    class="btn btn-outline-secondary btn-sm"
                    @click="aplicarPlantilla(p)"
                  >
                    ⚡ {{ p.titulo }}
                  </button>
                </div>
              </div>

              <!-- Formulario de Respuesta -->
              <div class="mb-3">
                <label class="form-label fw-semibold">Asunto del Correo *</label>
                <input
                  v-model="formRespuesta.asunto"
                  type="text"
                  required
                  class="form-control"
                  placeholder="Ej: Propuesta técnica para evento corporativo — Orion Stage"
                />
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Cuerpo del Mensaje *</label>
                <textarea
                  v-model="formRespuesta.mensaje"
                  rows="8"
                  required
                  class="form-control"
                  placeholder="Escribe aquí el mensaje oficial..."
                ></textarea>
              </div>

              <div class="row g-3 align-items-center mb-3">
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Actualizar estado tras enviar a:</label>
                  <select v-model="formRespuesta.nuevo_estado" class="form-select form-select-sm">
                    <option value="en_contacto">En contacto</option>
                    <option value="cotizado">Cotizado</option>
                    <option value="cerrado">Cerrado</option>
                    <option value="descartado">Descartado</option>
                  </select>
                </div>
              </div>

              <!-- Alertas de Envío -->
              <div v-if="errorRespuesta" class="alert alert-danger py-2 mb-3">{{ errorRespuesta }}</div>
              <div v-if="respuestaExitosa" class="alert alert-success py-2 mb-3">✓ {{ respuestaExitosa }}</div>
            </div>
          </div>

          <!-- FOOTER DEL MODAL -->
          <div class="modal-footer border-top border-secondary border-opacity-25 d-flex justify-content-between">
            <div>
              <button
                v-if="pestanaModal === 'responder'"
                type="button"
                class="btn btn-outline-secondary btn-sm me-2"
                @click="pestanaModal = 'detalle'"
              >
                ← Volver al detalle
              </button>
              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="eliminarCotizacion(cotizacionSeleccionada)"
              >
                Eliminar Cotización
              </button>
            </div>

            <div class="d-flex gap-2">
              <button type="button" class="btn btn-outline-secondary" @click="cerrarModal">Cerrar</button>
              <button
                v-if="pestanaModal === 'detalle'"
                type="button"
                class="btn btn-orion"
                @click="pestanaModal = 'responder'"
              >
                ✉ Redactar Respuesta
              </button>
              <button
                v-else
                type="button"
                class="btn btn-orion"
                :disabled="enviandoRespuesta"
                @click="enviarRespuesta"
              >
                <span v-if="enviandoRespuesta" class="spinner-border spinner-border-sm me-1" role="status"></span>
                {{ enviandoRespuesta ? 'Enviando correo...' : 'Enviar Correo al Cliente' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-mensajes-container {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
