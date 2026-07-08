import { api } from './api';
import type { Servicio, CategoriaServicio } from '@/types';

export const serviciosService = {
  async getCategorias(): Promise<CategoriaServicio[]> {
    const { data } = await api.get('/categorias-servicio/');
    return data;
  },
  async getServicios(categoriaSlug?: string): Promise<Servicio[]> {
    const { data } = await api.get('/servicios/', {
      params: categoriaSlug ? { categoria: categoriaSlug } : {},
    });
    return data;
  },
  async getServicioById(id: string): Promise<Servicio> {
    const { data } = await api.get(`/servicios/${id}/`);
    return data;
  },
};
