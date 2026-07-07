import { Router } from 'express';
import { supabase } from '../supabase.js';

export const blogRouter = Router();

blogRouter.get('/posts', async (req, res) => {
  const limit = Number(req.query.limit) || 9;
  const offset = Number(req.query.offset) || 0;

  let query = supabase
    .from('posts')
    .select('*, tags:post_tags(*)')
    .eq('estado', 'publicado')
    .order('fecha_publicacion', { ascending: false })
    .range(offset, offset + limit - 1);

  const tag = req.query.tag;
  if (typeof tag === 'string') {
    query = query.eq('tags.slug', tag);
  }

  const { data, error } = await query;
  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

blogRouter.get('/tags', async (_req, res) => {
  const { data, error } = await supabase
    .from('tags')
    .select('*')
    .order('nombre', { ascending: true });

  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

blogRouter.get('/posts/:slug', async (req, res) => {
  const { data, error } = await supabase
    .from('posts')
    .select('*, tags:post_tags(*)')
    .eq('slug', req.params.slug)
    .eq('estado', 'publicado')
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!data) return res.status(404).json({ error: 'Post no encontrado' });
  res.json(data);
});
