import { Router } from 'express';
import { supabase } from '../supabase.js';

export const serviciosRouter = Router();

serviciosRouter.get('/categorias', async (_req, res) => {
  const { data, error } = await supabase
    .from('categorias_servicio')
    .select('*')
    .order('orden', { ascending: true });

  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

serviciosRouter.get('/', async (req, res) => {
  let query = supabase
    .from('servicios')
    .select('*')
    .eq('activo', true)
    .order('orden', { ascending: true });

  const categoria = req.query.categoria;
  if (typeof categoria === 'string') {
    query = query.eq('categoria_slug', categoria);
  }

  const { data, error } = await query;
  if (error) return res.status(500).json({ error: error.message });
  res.json(data || []);
});

serviciosRouter.get('/:id', async (req, res) => {
  const { data, error } = await supabase
    .from('servicios')
    .select('*')
    .eq('id', req.params.id)
    .eq('activo', true)
    .maybeSingle();

  if (error) return res.status(500).json({ error: error.message });
  if (!data) return res.status(404).json({ error: 'Servicio no encontrado' });
  res.json(data);
});
