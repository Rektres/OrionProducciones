export interface CategoriaServicio {
  id: string;
  nombre: string;
  slug: string;
  orden: number;
  created_at: string;
}

export interface Servicio {
  id: string;
  categoria: string | null;
  categoria_slug: string | null;
  nombre: string;
  descripcion_corta: string;
  descripcion_larga: string;
  imagen: string | null;
  imagen_archivo: string | null;
  imagen_url: string | null;
  icono_svg: string | null;
  activo: boolean;
  orden: number;
  created_at: string;
}

export interface FotoEvento {
  id: string;
  evento: string;
  imagen: string | null;
  imagen_archivo: string | null;
  imagen_url: string | null;
  descripcion: string | null;
  orden: number;
  created_at: string;
}

export interface EventoTipo {
  id: string;
  nombre: string;
  slug: string;
  created_at: string;
}

export interface Evento {
  id: string;
  nombre: string;
  slug: string;
  tipo: string | null;
  tipo_slug: string | null;
  cliente: string;
  descripcion_corta: string;
  descripcion_larga: string;
  imagen_destacada: string | null;
  imagen_archivo: string | null;
  imagen_url: string | null;
  fecha_realizacion: string;
  lugar: string;
  asistentes: number | null;
  destacado: boolean;
  publicado: boolean;
  orden: number;
  created_at: string;
  fotos?: FotoEvento[];
}

export interface Tag {
  id: string;
  nombre: string;
  slug: string;
  created_at: string;
}

export interface Post {
  id: string;
  titulo: string;
  slug: string;
  imagen_destacada: string | null;
  imagen_archivo: string | null;
  imagen_url: string | null;
  extracto: string;
  contenido: string;
  estado: 'borrador' | 'revision' | 'publicado';
  fecha_publicacion: string | null;
  created_at: string;
  updated_at: string;
  tags?: Tag[];
}

export type TipoEvento = 'corporativo' | 'social' | 'festival' | 'otro';
export type EstadoCotizacion = 'nuevo' | 'en_contacto' | 'cotizado' | 'cerrado' | 'descartado';

export interface CotizacionHistorial {
  id: string;
  cotizacion: string;
  usuario: number | null;
  usuario_nombre: string;
  tipo_accion: string;
  estado_anterior: EstadoCotizacion | null;
  estado_nuevo: EstadoCotizacion | null;
  detalle: string | null;
  created_at: string;
}

export interface Cotizacion {
  id: string;
  nombre: string;
  email: string;
  telefono: string | null;
  empresa: string | null;
  tipo_evento: TipoEvento;
  descripcion: string;
  fecha_estimada: string | null;
  presupuesto_estimado: string | null;
  estado: EstadoCotizacion;
  created_at: string;
  historial?: CotizacionHistorial[];
}

export interface ResponderCotizacionInput {
  asunto: string;
  mensaje: string;
  nuevo_estado?: EstadoCotizacion;
}


export interface CotizacionFormData {
  nombre: string;
  email: string;
  telefono?: string;
  empresa?: string;
  tipo_evento: TipoEvento;
  descripcion: string;
  fecha_estimada?: string;
  presupuesto_estimado?: string;
}


// --- Tipos de entrada para el panel de administracion ---
// No incluyen los campos derivados/read-only (categoria_slug, tipo_slug,
// imagen_archivo, created_at, etc.) que el servidor calcula solo.

export interface ServicioInput {
  nombre: string;
  categoria: string | null;
  descripcion_corta: string;
  descripcion_larga: string;
  icono_svg: string | null;
  activo: boolean;
  orden: number;
}

export interface EventoInput {
  nombre: string;
  slug: string;
  tipo: string | null;
  cliente: string;
  descripcion_corta: string;
  descripcion_larga: string;
  fecha_realizacion: string;
  lugar: string;
  asistentes: number | null;
  destacado: boolean;
  publicado: boolean;
  orden: number;
}

export interface PostInput {
  titulo: string;
  slug: string;
  extracto: string;
  contenido: string;
  estado: 'borrador' | 'revision' | 'publicado';
  fecha_publicacion: string | null;
  tags: string[];
}
