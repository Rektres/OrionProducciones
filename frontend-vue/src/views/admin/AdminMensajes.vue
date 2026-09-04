<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { adminCotizacionesService } from '@/services/adminCotizaciones';
import type { Cotizacion, EstadoCotizacion, ResponderCotizacionInput } from '@/types';

const cotizaciones = ref<Cotizacion[]>([]);
const cargando = ref(false);
const busqueda = ref('');
const filtroEstado = ref<string>('todos');
const vista = ref<'lista' | 'cards'>('lista');

// Ordenamiento de tabla
type ColumnaOrden = 'estado' | 'created_at' | 'nombre' | 'tipo_evento' | 'fecha_estimada' | 'presupuesto_estimado';
const columnaOrden = ref<ColumnaOrden>('created_at');
const direccionOrden = ref<'asc' | 'desc'>('desc');

const ordenarPor = (col: ColumnaOrden) => {
  if (columnaOrden.value === col) {
    direccionOrden.value = direccionOrden.value === 'asc' ? 'desc' : 'asc';
  } else {
    columnaOrden.value = col;
    direccionOrden.value = 'asc';
  }
};

// Modal de detalle, respuesta e historial
const modalAbierto = ref(false);
const cotizacionSeleccionada = ref<Cotizacion | null>(null);
const pestanaModal = ref<'detalle' | 'responder' | 'historial'>('detalle');

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
    if (cotizacionSeleccionada.value) {
      const updated = cotizaciones.value.find((c) => c.id === cotizacionSeleccionada.value?.id);
      if (updated) cotizacionSeleccionada.value = { ...updated };
    }
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

// Filtrado y ordenamiento reactivo
const filtradasYOrdenadas = computed(() => {
  let list = [...cotizaciones.value];

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

  const factor = direccionOrden.value === 'asc' ? 1 : -1;
  list.sort((a, b) => {
    switch (columnaOrden.value) {
      case 'created_at':
        return factor * (new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
      case 'nombre':
        return factor * a.nombre.localeCompare(b.nombre, 'es');
      case 'tipo_evento':
        return factor * a.tipo_evento.localeCompare(b.tipo_evento, 'es');
      case 'fecha_estimada': {
        const fa = a.fecha_estimada || '';
        const fb = b.fecha_estimada || '';
        return factor * fa.localeCompare(fb);
      }
      case 'presupuesto_estimado': {
        const pa = a.presupuesto_estimado || '';
        const pb = b.presupuesto_estimado || '';
        return factor * pa.localeCompare(pb);
      }
      case 'estado':
        return factor * a.estado.localeCompare(b.estado);
      default:
        return 0;
    }
  });

  return list;
});

const abrirDetalle = (c: Cotizacion, tab: 'detalle' | 'responder' | 'historial' = 'detalle') => {
  cotizacionSeleccionada.value = { ...c };
  pestanaModal.value = tab;
  errorRespuesta.value = '';
  respuestaExitosa.value = '';

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
    cotizacionSeleccionada.value = { ...actualizada };
    const idx = cotizaciones.value.findIndex((c) => c.id === actualizada.id);
    if (idx !== -1) cotizaciones.value[idx] = actualizada;
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
    cotizacionSeleccionada.value = { ...res.cotizacion };

    // Actualizar en listado general
    const idx = cotizaciones.value.findIndex((c) => c.id === res.cotizacion.id);
    if (idx !== -1) cotizaciones.value[idx] = res.cotizacion;

    setTimeout(() => {
      pestanaModal.value = 'historial';
    }, 1500);
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

// Clases sobrias y no neón para estados
const badgeClaseEstado = (estado: EstadoCotizacion) => {
  switch (estado) {
    case 'nuevo':
      return 'badge-subtle-amber';
    case 'en_contacto':
      return 'badge-subtle-sky';
    case 'cotizado':
      return 'badge-subtle-indigo';
    case 'cerrado':
      return 'badge-subtle-emerald';
    case 'descartado':
      return 'badge-subtle-slate';
    default:
      return 'badge-subtle-slate';
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

const labelTipoAccion = (tipo: string) => {
  switch (tipo) {
    case 'creacion':
      return 'Registro Web';
    case 'cambio_estado':
      return 'Cambio de Estado';
    case 'respuesta_correo':
      return 'Correo Oficial';
    case 'nota':
      return 'Nota Interna';
    default:
      return tipo;
  }
};

const badgeClaseAccion = (tipo: string) => {
  switch (tipo) {
    case 'creacion':
      return 'badge-subtle-slate';
    case 'cambio_estado':
      return 'badge-subtle-sky';
    case 'respuesta_correo':
      return 'badge-subtle-indigo';
    default:
      return 'badge-subtle-slate';
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
          Gestiona requerimientos, revisa el historial de auditoría y responde oficialmente desde <strong>contacto@orionstage.cl</strong>.
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
          :class="{ 'border-primary-subtle shadow-sm active-tab-border': filtroEstado === 'todos' }"
          @click="filtroEstado = 'todos'"
        >
          <small class="text-secondary d-block text-uppercase" style="font-size: 11px;">Total</small>
          <span class="fs-4 fw-bold text-body">{{ cotizaciones.length }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-warning-subtle shadow-sm active-tab-border': filtroEstado === 'nuevo' }"
          @click="filtroEstado = 'nuevo'"
        >
          <small class="text-warning-emphasis d-block text-uppercase" style="font-size: 11px;">● Nuevos</small>
          <span class="fs-4 fw-bold text-warning-emphasis">{{ totalNuevos }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-info-subtle shadow-sm active-tab-border': filtroEstado === 'en_contacto' }"
          @click="filtroEstado = 'en_contacto'"
        >
          <small class="text-info-emphasis d-block text-uppercase" style="font-size: 11px;">En contacto</small>
          <span class="fs-4 fw-bold text-info-emphasis">{{ totalEnContacto }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-indigo-subtle shadow-sm active-tab-border': filtroEstado === 'cotizado' }"
          @click="filtroEstado = 'cotizado'"
        >
          <small class="text-primary-emphasis d-block text-uppercase" style="font-size: 11px;">Cotizados</small>
          <span class="fs-4 fw-bold text-primary-emphasis">{{ totalCotizados }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-success-subtle shadow-sm active-tab-border': filtroEstado === 'cerrado' }"
          @click="filtroEstado = 'cerrado'"
        >
          <small class="text-success-emphasis d-block text-uppercase" style="font-size: 11px;">✓ Cerrados</small>
          <span class="fs-4 fw-bold text-success-emphasis">{{ totalCerrados }}</span>
        </div>
      </div>
      <div class="col-6 col-md-4 col-lg-2">
        <div
          class="card admin-card p-3 text-center admin-card-clickable h-100"
          :class="{ 'border-secondary shadow-sm active-tab-border': filtroEstado === 'descartado' }"
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
        <div class="flex-grow-1" style="max-width: 380px;">
          <input
            v-model="busqueda"
            type="search"
            class="form-control form-control-sm admin-toolbar-search"
            placeholder="Buscar cliente, email, empresa..."
          />
        </div>

        <!-- Filtros Chips -->
        <div class="d-flex gap-1 flex-wrap align-items-center">
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'todos' ? 'btn-secondary fw-bold text-white' : 'btn-outline-secondary'"
            @click="filtroEstado = 'todos'"
          >
            Todos
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'nuevo' ? 'badge-estado-nuevo fw-bold text-white shadow-sm' : 'btn-outline-secondary'"
            @click="filtroEstado = 'nuevo'"
          >
            ● Nuevos ({{ totalNuevos }})
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'en_contacto' ? 'badge-estado-contacto fw-bold text-white shadow-sm' : 'btn-outline-secondary'"
            @click="filtroEstado = 'en_contacto'"
          >
            En contacto ({{ totalEnContacto }})
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'cotizado' ? 'badge-estado-cotizado fw-bold text-white shadow-sm' : 'btn-outline-secondary'"
            @click="filtroEstado = 'cotizado'"
          >
            Cotizados ({{ totalCotizados }})
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="filtroEstado === 'cerrado' ? 'badge-estado-cerrado fw-bold text-white shadow-sm' : 'btn-outline-secondary'"
            @click="filtroEstado = 'cerrado'"
          >
            ✓ Cerrados ({{ totalCerrados }})
          </button>
        </div>

        <!-- Selector de Vista Cards / Lista -->
        <div class="btn-group btn-group-sm ms-auto" role="group" aria-label="Cambiar vista">
          <button
            type="button"
            class="btn"
            :class="vista === 'lista' ? 'btn-secondary' : 'btn-outline-secondary'"
            title="Vista en lista"
            @click="vista = 'lista'"
          >
            ☰ Lista
          </button>
          <button
            type="button"
            class="btn"
            :class="vista === 'cards' ? 'btn-secondary' : 'btn-outline-secondary'"
            title="Vista en tarjetas"
            @click="vista = 'cards'"
          >
            ⊞ Tarjetas
          </button>
        </div>
      </div>
    </div>

    <!-- LISTADO - VISTA 1: TABLA (LISTA) CON SORTING -->
    <div v-if="vista === 'lista'" class="card admin-card overflow-hidden shadow-sm">
      <div class="table-responsive mb-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-dark">
            <tr>
              <th style="width: 130px; cursor: pointer; user-select: none;" @click="ordenarPor('estado')">
                Estado
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'estado' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="width: 160px; cursor: pointer; user-select: none;" @click="ordenarPor('created_at')">
                Fecha / Hora
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'created_at' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="cursor: pointer; user-select: none;" @click="ordenarPor('nombre')">
                Cliente / Empresa
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'nombre' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="cursor: pointer; user-select: none;" @click="ordenarPor('tipo_evento')">
                Tipo Evento
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'tipo_evento' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="cursor: pointer; user-select: none;" @click="ordenarPor('fecha_estimada')">
                Fecha Est.
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'fecha_estimada' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="cursor: pointer; user-select: none;" @click="ordenarPor('presupuesto_estimado')">
                Presupuesto
                <span class="small opacity-75 ms-1">{{ columnaOrden === 'presupuesto_estimado' ? (direccionOrden === 'asc' ? '▲' : '▼') : '↕' }}</span>
              </th>
              <th style="width: 250px;" class="text-end text-nowrap">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in filtradasYOrdenadas"
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
                <span class="badge badge-subtle-slate text-uppercase" style="font-size: 11px;">
                  {{ c.tipo_evento }}
                </span>
              </td>
              <td>
                <small>{{ c.fecha_estimada || 'Por definir' }}</small>
              </td>
              <td>
                <span v-if="c.presupuesto_estimado" class="text-success-emphasis small fw-semibold">
                  {{ c.presupuesto_estimado }}
                </span>
                <span v-else class="text-secondary small">-</span>
              </td>
              <!-- ACCIONES ALINEADAS HORIZONTALMENTE CON ELIMINAR A LA DERECHA -->
              <td class="text-end text-nowrap" @click.stop>
                <div class="d-inline-flex align-items-center gap-1">
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm"
                    title="Ver detalle del requerimiento"
                    @click="abrirDetalle(c, 'detalle')"
                  >
                    👁 Ver
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-primary btn-sm"
                    title="Responder por correo oficial"
                    @click="abrirDetalle(c, 'responder')"
                  >
                    ✉ Responder
                  </button>
                  <a
                    v-if="c.telefono"
                    :href="obtenerLinkWhatsapp(c)"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="btn btn-outline-success btn-sm"
                    title="Abrir WhatsApp"
                  >
                    WhatsApp
                  </a>
                  <button
                    type="button"
                    class="btn btn-outline-danger btn-sm"
                    title="Eliminar cotización"
                    @click="eliminarCotizacion(c)"
                  >
                    ✕
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!filtradasYOrdenadas.length">
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
      <div v-for="c in filtradasYOrdenadas" :key="c.id" class="col-md-6 col-lg-4">
        <div
          class="card h-100 admin-card admin-card-clickable p-3 d-flex flex-column justify-content-between"
          :class="{ 'border-warning-subtle': c.estado === 'nuevo' }"
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
              <span class="badge badge-subtle-slate text-uppercase" style="font-size: 10px;">
                {{ c.tipo_evento }}
              </span>
              <span v-if="c.fecha_estimada" class="badge badge-subtle-slate" style="font-size: 10px;">
                📅 {{ c.fecha_estimada }}
              </span>
              <span v-if="c.historial && c.historial.length" class="badge badge-subtle-sky ms-auto" style="font-size: 10px;">
                📜 {{ c.historial.length }} eventos
              </span>
            </div>

            <p class="small text-body bg-dark bg-opacity-40 p-2 rounded mb-3" style="max-height: 70px; overflow: hidden; text-overflow: ellipsis; line-height: 1.5;">
              "{{ c.descripcion }}"
            </p>
          </div>

          <!-- BARRA DE ACCIONES DE TARJETA -->
          <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-25" @click.stop>
            <a
              v-if="c.telefono"
              :href="obtenerLinkWhatsapp(c)"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-outline-success btn-sm py-1 px-2"
              title="Abrir WhatsApp"
            >
              WhatsApp
            </a>
            <div class="d-inline-flex gap-1 ms-auto">
              <button
                type="button"
                class="btn btn-outline-secondary btn-sm py-1 px-2"
                @click="abrirDetalle(c, 'detalle')"
              >
                👁 Ver
              </button>
              <button
                type="button"
                class="btn btn-outline-primary btn-sm py-1 px-2"
                @click="abrirDetalle(c, 'responder')"
              >
                ✉ Responder
              </button>
              <button
                type="button"
                class="btn btn-outline-danger btn-sm py-1 px-2"
                title="Eliminar"
                @click="eliminarCotizacion(c)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!filtradasYOrdenadas.length" class="col-12 text-center py-5 text-secondary">
        {{ cotizaciones.length ? `No hay mensajes que coincidan con "${busqueda}".` : 'No se han recibido mensajes aún.' }}
      </div>
    </div>

    <!-- MODAL DE DETALLE, RESPUESTA E HISTORIAL -->
    <div
      v-if="modalAbierto && cotizacionSeleccionada"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.85); z-index: 1060; backdrop-filter: blur(4px);"
      @click.self="cerrarModal"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
        <div class="modal-content admin-card border border-secondary border-opacity-25 shadow-lg">
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

          <!-- PESTAÑAS DENTRO DEL MODAL (DETALLE / RESPONDER / HISTORIAL) -->
          <div class="px-4 pt-3 border-bottom border-secondary border-opacity-25">
            <ul class="nav nav-tabs border-0 gap-2">
              <li class="nav-item">
                <button
                  type="button"
                  class="nav-link py-2 px-3"
                  :class="{ 'active fw-bold text-orion-gold': pestanaModal === 'detalle' }"
                  @click="pestanaModal = 'detalle'"
                >
                  📋 Detalle del Requerimiento
                </button>
              </li>
              <li class="nav-item">
                <button
                  type="button"
                  class="nav-link py-2 px-3"
                  :class="{ 'active fw-bold text-orion-gold': pestanaModal === 'responder' }"
                  @click="pestanaModal = 'responder'"
                >
                  ✉ Redactar Respuesta
                </button>
              </li>
              <li class="nav-item">
                <button
                  type="button"
                  class="nav-link py-2 px-3"
                  :class="{ 'active fw-bold text-orion-gold': pestanaModal === 'historial' }"
                  @click="pestanaModal = 'historial'"
                >
                  📜 Historial & Auditoría
                  <span v-if="cotizacionSeleccionada.historial && cotizacionSeleccionada.historial.length" class="badge badge-subtle-slate ms-1">
                    {{ cotizacionSeleccionada.historial.length }}
                  </span>
                </button>
              </li>
            </ul>
          </div>

          <!-- CUERPO DEL MODAL -->
          <div class="modal-body p-4">
            <!-- PESTAÑA 1: DETALLE DE COTIZACIÓN -->
            <div v-if="pestanaModal === 'detalle'">
              <!-- Ficha de Datos -->
              <div class="card bg-dark bg-opacity-40 border border-secondary border-opacity-25 p-3 mb-4 rounded-3">
                <div class="row g-3">
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Correo Electrónico</small>
                    <a :href="`mailto:${cotizacionSeleccionada.email}`" class="text-primary-emphasis fw-semibold">
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
                        class="badge badge-subtle-emerald text-decoration-none py-1 px-2"
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
                    <span class="badge badge-subtle-slate text-uppercase">{{ cotizacionSeleccionada.tipo_evento }}</span>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Fecha Estimada</small>
                    <span class="fw-semibold">{{ cotizacionSeleccionada.fecha_estimada || 'Por coordinar' }}</span>
                  </div>
                  <div class="col-sm-6">
                    <small class="text-secondary d-block">Presupuesto Estimado</small>
                    <span class="fw-bold text-success-emphasis">{{ cotizacionSeleccionada.presupuesto_estimado || 'A evaluar' }}</span>
                  </div>
                </div>
              </div>

              <!-- Mensaje / Requerimiento -->
              <h6 class="fw-bold mb-2 text-orion-gold">Mensaje o Detalle del Requerimiento:</h6>
              <div class="p-3 bg-dark bg-opacity-50 rounded-3 border-start border-3 border-warning-subtle mb-4" style="white-space: pre-wrap; font-size: 14.5px; line-height: 1.7;">
{{ cotizacionSeleccionada.descripcion }}
              </div>

              <!-- Selector Rápido de Estado -->
              <div class="card p-3 bg-dark bg-opacity-40 border border-secondary border-opacity-25 rounded-3">
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
            <div v-else-if="pestanaModal === 'responder'">
              <div class="alert alert-secondary py-2 px-3 small mb-3 border border-secondary border-opacity-25 bg-dark bg-opacity-50">
                ℹ El mensaje será enviado formalmente desde <strong>contacto@orionstage.cl</strong> a <strong>{{ cotizacionSeleccionada.email }}</strong> respetando todos los párrafos y saltos de línea.
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
                  placeholder="Escribe aquí el mensaje oficial respetando los párrafos..."
                  style="line-height: 1.6; font-size: 14.5px;"
                ></textarea>
                <small class="text-secondary d-block mt-1">
                  💡 Los saltos de línea y párrafos escritos aquí se reflejarán fielmente en el correo final del cliente.
                </small>
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

            <!-- PESTAÑA 3: HISTORIAL & AUDITORÍA -->
            <div v-else-if="pestanaModal === 'historial'">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold mb-0 text-orion-gold">Registro de Acciones y Cambios de Estado</h6>
                <small class="text-secondary">Total: {{ cotizacionSeleccionada.historial?.length || 0 }} registros</small>
              </div>

              <div v-if="cotizacionSeleccionada.historial && cotizacionSeleccionada.historial.length" class="timeline-container">
                <div
                  v-for="(h, idx) in cotizacionSeleccionada.historial"
                  :key="h.id || idx"
                  class="timeline-item pb-3 mb-3 border-bottom border-secondary border-opacity-10"
                >
                  <div class="d-flex justify-content-between align-items-start mb-1">
                    <div class="d-flex align-items-center gap-2">
                      <span class="badge" :class="badgeClaseAccion(h.tipo_accion)">
                        {{ labelTipoAccion(h.tipo_accion) }}
                      </span>
                      <strong class="small text-body">{{ h.usuario_nombre || 'Admin' }}</strong>
                    </div>
                    <small class="text-secondary">{{ formatearFecha(h.created_at) }}</small>
                  </div>

                  <p class="small text-body mb-1" style="line-height: 1.5;">
                    {{ h.detalle }}
                  </p>

                  <div v-if="h.estado_anterior || h.estado_nuevo" class="d-flex align-items-center gap-1 mt-1">
                    <small class="text-secondary" style="font-size: 11px;">Transición:</small>
                    <span v-if="h.estado_anterior" class="badge badge-subtle-slate" style="font-size: 10px;">
                      {{ labelEstado(h.estado_anterior) }}
                    </span>
                    <span class="text-secondary" style="font-size: 10px;">➔</span>
                    <span v-if="h.estado_nuevo" class="badge" :class="badgeClaseEstado(h.estado_nuevo)" style="font-size: 10px;">
                      {{ labelEstado(h.estado_nuevo) }}
                    </span>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-4 text-secondary">
                No hay registros de historial previos para esta cotización.
              </div>
            </div>
          </div>

          <!-- FOOTER DEL MODAL -->
          <div class="modal-footer border-top border-secondary border-opacity-25 d-flex justify-content-between">
            <div>
              <button
                v-if="pestanaModal !== 'detalle'"
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
                class="btn btn-outline-primary"
                @click="pestanaModal = 'responder'"
              >
                ✉ Redactar Respuesta
              </button>
              <button
                v-else-if="pestanaModal === 'responder'"
                type="button"
                class="btn btn-primary"
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

.active-tab-border {
  border-color: #d06c26 !important;
  background: rgba(208, 108, 38, 0.08);
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
