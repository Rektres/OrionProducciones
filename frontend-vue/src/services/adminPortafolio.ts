import { api } from './api';
import type { Evento, EventoInput, EventoTipo, FotoEvento } from '@/types';

export const adminPortafolioService = {
  async listarTipos(): Promise<EventoTipo[]> {
    const { data } = await api.get('/admin/evento-tipos/');
    return data;
  },

  async listar(): Promise<Evento[]> {
    const { data } = await api.get('/admin/eventos/');
    return data;
  },

  async crear(input: EventoInput): Promise<Evento> {
    const { data } = await api.post('/admin/eventos/', input);
    return data;
  },

  async actualizar(id: string, input: Partial<EventoInput>): Promise<Evento> {
    const { data } = await api.patch(`/admin/eventos/${id}/`, input);
    return data;
  },

  async eliminar(id: string): Promise<void> {
    await api.delete(`/admin/eventos/${id}/`);
  },

  async subirImagen(id: string, archivo: File): Promise<Evento> {
    const form = new FormData();
    form.append('archivo', archivo);
    const { data } = await api.post(`/admin/eventos/${id}/imagen/`, form);
    return data;
  },

  async quitarImagen(id: string): Promise<Evento> {
    const { data } = await api.delete(`/admin/eventos/${id}/imagen/`);
    return data;
  },

  async listarFotos(eventoId: string): Promise<FotoEvento[]> {
    const { data } = await api.get(`/admin/eventos/${eventoId}/fotos/`);
    return data;
  },

  async agregarFoto(eventoId: string, archivo: File, descripcion?: string, orden?: number): Promise<FotoEvento> {
    const form = new FormData();
    form.append('archivo', archivo);
    if (descripcion) form.append('descripcion', descripcion);
    if (orden !== undefined) form.append('orden', String(orden));
    const { data } = await api.post(`/admin/eventos/${eventoId}/fotos/`, form);
    return data;
  },

  async eliminarFoto(fotoId: string): Promise<void> {
    await api.delete(`/admin/fotos-evento/${fotoId}/`);
  },
};
