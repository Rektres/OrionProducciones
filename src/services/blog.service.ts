import { supabase } from '@/lib/supabase';
import { Post, Tag } from '@/types';

export const blogService = {
  async getPosts(limit: number = 9, offset: number = 0): Promise<Post[]> {
    const { data, error } = await supabase
      .from('posts')
      .select('*, tags:post_tags(*)')
      .eq('estado', 'publicado')
      .order('fecha_publicacion', { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) throw error;
    return data || [];
  },

  async getPostBySlug(slug: string): Promise<Post | null> {
    const { data, error } = await supabase
      .from('posts')
      .select('*, tags:post_tags(*)')
      .eq('slug', slug)
      .eq('estado', 'publicado')
      .maybeSingle();

    if (error) throw error;
    return data;
  },

  async getTags(): Promise<Tag[]> {
    const { data, error } = await supabase
      .from('tags')
      .select('*')
      .order('nombre', { ascending: true });

    if (error) throw error;
    return data || [];
  },

  async getPostsByTag(tagSlug: string, limit: number = 9, offset: number = 0): Promise<Post[]> {
    const { data, error } = await supabase
      .from('posts')
      .select('*, tags:post_tags(*)')
      .eq('estado', 'publicado')
      .eq('tags.slug', tagSlug)
      .order('fecha_publicacion', { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) throw error;
    return data || [];
  },
};
