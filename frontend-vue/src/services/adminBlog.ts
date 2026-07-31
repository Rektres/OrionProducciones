import { api } from './api';
import type { Post, PostInput, Tag } from '@/types';

export const adminBlogService = {
  async listarTags(): Promise<Tag[]> {
    const { data } = await api.get('/admin/tags/');
    return data;
  },

  async crearTag(nombre: string, slug: string): Promise<Tag> {
    const { data } = await api.post('/admin/tags/', { nombre, slug });
    return data;
  },

  async listar(): Promise<Post[]> {
    const { data } = await api.get('/admin/posts/');
    return data;
  },

  async crear(input: PostInput): Promise<Post> {
    const { data } = await api.post('/admin/posts/', input);
    return data;
  },

  async actualizar(id: string, input: Partial<PostInput>): Promise<Post> {
    const { data } = await api.patch(`/admin/posts/${id}/`, input);
    return data;
  },

  async eliminar(id: string): Promise<void> {
    await api.delete(`/admin/posts/${id}/`);
  },

  async subirImagen(id: string, archivo: File): Promise<Post> {
    const form = new FormData();
    form.append('archivo', archivo);
    const { data } = await api.post(`/admin/posts/${id}/imagen/`, form);
    return data;
  },

  async quitarImagen(id: string): Promise<Post> {
    const { data } = await api.delete(`/admin/posts/${id}/imagen/`);
    return data;
  },
};
