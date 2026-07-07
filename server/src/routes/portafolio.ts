import { Router } from 'express';
import { supabase } from '../supabase.js';

export const portafolioRouter = Router();

portafolioRouter.get('/tipos', async (_req, res) => {
  const { data, error } = await supabase
    .from('evento_tipos')
    .select('*')
    .order('nombre', { ascending: true });

  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

portafolioRouter.get('/eventos', async (req, res) => {
  let query = supabase
    .from('eventos')
    .select('*, fotos:fotos_evento(*)')
    .eq('publicado', true)
    .order('fecha_realizacion', { ascending: false });

  const tipo = req.query.tipo;
  if (typeof tipo === 'string') {
    query = query.eq('tipo_slug', tipo);
  }

  const destacado = req.query.destacado;
  if (destacado === 'true' || destacado === 'false') {
    query = query.eq('destacado', destacado === 'true');
  }

  const { data, error } = await query;
  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

portafolioRouter.get('/eventos/:id/fotos', async (req, res) => {
  const { data, error } = await supabase
    .from('fotos_evento')
    .select('*')
    .eq('evento_id', req.params.id)
    .order('orden', { ascending: true });

  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

portafolioRouter.get('/eventos/:slug', async (req, res) => {
  const { data, error } = await supabase
    .from('eventos')
    .select('*, fotos:fotos_evento(*)')
    .eq('slug', req.params.slug)
    .eq('publicado', true)
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!data) return res.status(404).json({ error: 'Evento no encontrado' });
  res.json(data);
});
