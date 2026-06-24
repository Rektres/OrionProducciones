import { supabase } from '@/lib/supabase';
import { Servicio, CategoriaServicio } from '@/types';

export const serviciosService = {
  async getCategorias(): Promise<CategoriaServicio[]> {
    const { data, error } = await supabase
      .from('categorias_servicio')
      .select('*')
      .order('orden', { ascending: true });

    if (error) throw error;
    return data || [];
  },

  async getServicios(categoriaSlug?: string): Promise<Servicio[]> {
    let query = supabase
      .from('servicios')
      .select('*')
      .eq('activo', true)
      .order('orden', { ascending: true });

    if (categoriaSlug) {
      query = query.eq('categoria_slug', categoriaSlug);
    }

    const { data, error } = await query;
    if (error) throw error;
    return data || [];
  },

  async getServicioById(id: string): Promise<Servicio | null> {
    const { data, error } = await supabase
      .from('servicios')
      .select('*')
      .eq('id', id)
      .maybeSingle();

    if (error) throw error;
    return data;
  },
};
