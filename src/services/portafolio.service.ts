import { supabase } from '@/lib/supabase';
import { Evento, EventoTipo, FotoEvento } from '@/types';

export const portafolioService = {
  async getTipos(): Promise<EventoTipo[]> {
    const { data, error } = await supabase
      .from('evento_tipos')
      .select('*')
      .order('nombre', { ascending: true });

    if (error) throw error;
    return data || [];
  },

  async getEventos(tipoSlug?: string, destacado?: boolean): Promise<Evento[]> {
    let query = supabase
      .from('eventos')
      .select('*, fotos:fotos_evento(*)')
      .eq('publicado', true)
      .order('fecha_realizacion', { ascending: false });

    if (tipoSlug) {
      query = query.eq('tipo_slug', tipoSlug);
    }

    if (destacado !== undefined) {
      query = query.eq('destacado', destacado);
    }

    const { data, error } = await query;
    if (error) throw error;
    return data || [];
  },

  async getEventoBySlug(slug: string): Promise<Evento | null> {
    const { data, error } = await supabase
      .from('eventos')
      .select('*, fotos:fotos_evento(*)')
      .eq('slug', slug)
      .eq('publicado', true)
      .maybeSingle();

    if (error) throw error;
    return data;
  },

  async getFotosEvento(eventoId: string): Promise<FotoEvento[]> {
    const { data, error } = await supabase
      .from('fotos_evento')
      .select('*')
      .eq('evento_id', eventoId)
      .order('orden', { ascending: true });

    if (error) throw error;
    return data || [];
  },
};
