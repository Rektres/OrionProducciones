import { api } from './api';
import type { Evento, EventoTipo, FotoEvento } from '@/types';

export const portafolioService = {
  async getTipos(): Promise<EventoTipo[]> {
    const { data } = await api.get('/evento-tipos/');
    return data;
  },
  async getEventos(tipoSlug?: string, destacado?: boolean): Promise<Evento[]> {
    const params: Record<string, string> = {};
    if (tipoSlug) params.tipo = tipoSlug;
    if (destacado !== undefined) params.destacado = String(destacado);
    const { data } = await api.get('/eventos/', { params });
    return data;
  },
  async getEventoBySlug(slug: string): Promise<Evento> {
    const { data } = await api.get(`/eventos/${slug}/`);
    return data;
  },
  async getFotosEvento(eventoId: string): Promise<FotoEvento[]> {
    const { data } = await api.get(`/eventos/${eventoId}/fotos/`);
    return data;
  },
};
