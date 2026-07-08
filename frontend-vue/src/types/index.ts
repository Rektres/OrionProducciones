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
  icono_svg: string | null;
  activo: boolean;
  orden: number;
  created_at: string;
}

export interface FotoEvento {
  id: string;
  evento: string;
  imagen: string;
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
  extracto: string;
  contenido: string;
  estado: 'borrador' | 'revision' | 'publicado';
  fecha_publicacion: string | null;
  created_at: string;
  updated_at: string;
  tags?: Tag[];
}

export type TipoEvento = 'corporativo' | 'social' | 'festival' | 'otro';

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
