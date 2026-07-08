import { api } from './api';
import type { Post, Tag } from '@/types';

export const blogService = {
  async getPosts(limit = 9, offset = 0, tag?: string): Promise<Post[]> {
    const params: Record<string, string | number> = { limit, offset };
    if (tag) params.tag = tag;
    const { data } = await api.get('/posts/', { params });
    return data;
  },
  async getPostBySlug(slug: string): Promise<Post> {
    const { data } = await api.get(`/posts/${slug}/`);
    return data;
  },
  async getTags(): Promise<Tag[]> {
    const { data } = await api.get('/tags/');
    return data;
  },
};
