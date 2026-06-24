export interface Servicio {
  id: string;
  categoria_id: string;
  nombre: string;
  descripcion_corta: string;
  descripcion_larga: string;
  imagen: string;
  icono_svg: string;
  activo: boolean;
  orden: number;
  created_at: string;
}

export interface CategoriaServicio {
  id: string;
  nombre: string;
  slug: string;
  orden: number;
  created_at: string;
}

export interface Evento {
  id: string;
  nombre: string;
  slug: string;
  tipo_id: string;
  cliente: string;
  descripcion_corta: string;
  descripcion_larga: string;
  imagen_destacada: string;
  fecha_realizacion: string;
  lugar: string;
  asistentes: number | null;
  destacado: boolean;
  publicado: boolean;
  orden: number;
  created_at: string;
  fotos?: FotoEvento[];
}

export interface FotoEvento {
  id: string;
  evento_id: string;
  imagen: string;
  descripcion: string;
  orden: number;
  created_at: string;
}

export interface EventoTipo {
  id: string;
  nombre: string;
  slug: string;
  created_at: string;
}

export interface Post {
  id: string;
  titulo: string;
  slug: string;
  imagen_destacada: string;
  extracto: string;
  contenido: string;
  autor_id: string;
  estado: 'borrador' | 'revision' | 'publicado';
  fecha_publicacion: string | null;
  created_at: string;
  updated_at: string;
  tags?: Tag[];
}

export interface Tag {
  id: string;
  nombre: string;
  slug: string;
  created_at: string;
}

export interface Cotizacion {
  id: string;
  nombre: string;
  email: string;
  telefono: string;
  empresa: string;
  tipo_evento: 'corporativo' | 'social' | 'festival' | 'otro';
  descripcion: string;
  fecha_estimada: string | null;
  presupuesto_estimado: string;
  estado: 'nuevo' | 'en_contacto' | 'cotizado' | 'cerrado' | 'descartado';
  created_at: string;
}

export interface CotizacionFormData {
  nombre: string;
  email: string;
  telefono?: string;
  empresa?: string;
  tipo_evento: 'corporativo' | 'social' | 'festival' | 'otro';
  descripcion: string;
  fecha_estimada?: string;
  presupuesto_estimado?: string;
}

export interface Usuario {
  id: string;
  email: string;
  rol: 'admin' | 'visitante';
  created_at: string;
}
