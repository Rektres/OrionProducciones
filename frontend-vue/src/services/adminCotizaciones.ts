import { api } from './api';
import type { Cotizacion, EstadoCotizacion, ResponderCotizacionInput } from '@/types';

export const adminCotizacionesService = {
  async listar(params?: { estado?: string; search?: string }): Promise<Cotizacion[]> {
    const { data } = await api.get('/admin/cotizaciones/', { params });
    return data;
  },

  async obtener(id: string): Promise<Cotizacion> {
    const { data } = await api.get(`/admin/cotizaciones/${id}/`);
    return data;
  },

  async actualizarEstado(id: string, estado: EstadoCotizacion): Promise<Cotizacion> {
    const { data } = await api.patch(`/admin/cotizaciones/${id}/`, { estado });
    return data;
  },

  async responder(
    id: string,
    input: ResponderCotizacionInput
  ): Promise<{ status: string; mensaje: string; cotizacion: Cotizacion }> {
    const { data } = await api.post(`/admin/cotizaciones/${id}/responder/`, input);
    return data;
  },

  async eliminar(id: string): Promise<void> {
    await api.delete(`/admin/cotizaciones/${id}/`);
  },
};
