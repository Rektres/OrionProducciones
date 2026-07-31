import { api } from './api';
import type { CategoriaServicio, Servicio, ServicioInput } from '@/types';

export const adminServiciosService = {
  async listarCategorias(): Promise<CategoriaServicio[]> {
    const { data } = await api.get('/admin/categorias-servicio/');
    return data;
  },

  async crearCategoria(nombre: string, slug: string): Promise<CategoriaServicio> {
    const { data } = await api.post('/admin/categorias-servicio/', { nombre, slug, orden: 0 });
    return data;
  },

  async eliminarCategoria(id: string): Promise<void> {
    await api.delete(`/admin/categorias-servicio/${id}/`);
  },

  async listar(): Promise<Servicio[]> {
    const { data } = await api.get('/admin/servicios/');
    return data;
  },

  async crear(input: ServicioInput): Promise<Servicio> {
    const { data } = await api.post('/admin/servicios/', input);
    return data;
  },

  async actualizar(id: string, input: Partial<ServicioInput>): Promise<Servicio> {
    const { data } = await api.patch(`/admin/servicios/${id}/`, input);
    return data;
  },

  async eliminar(id: string): Promise<void> {
    await api.delete(`/admin/servicios/${id}/`);
  },

  async subirImagen(id: string, archivo: File): Promise<Servicio> {
    const form = new FormData();
    form.append('archivo', archivo);
    const { data } = await api.post(`/admin/servicios/${id}/imagen/`, form);
    return data;
  },

  async quitarImagen(id: string): Promise<Servicio> {
    const { data } = await api.delete(`/admin/servicios/${id}/imagen/`);
    return data;
  },
};
