import { Router } from 'express';
import { supabase } from '../supabase.js';

export const cotizacionesRouter = Router();

const TIPOS_EVENTO = ['corporativo', 'social', 'festival', 'otro'];

cotizacionesRouter.post('/', async (req, res) => {
  const body = req.body ?? {};
  const { nombre, email, tipo_evento, descripcion } = body;

  if (!nombre || !email || !descripcion) {
    return res.status(400).json({ error: 'nombre, email y descripcion son requeridos' });
  }
  if (!TIPOS_EVENTO.includes(tipo_evento)) {
    return res.status(400).json({ error: `tipo_evento debe ser uno de: ${TIPOS_EVENTO.join(', ')}` });
  }

  const { data, error } = await supabase
    .from('cotizaciones')
    .insert([
      {
        nombre,
        email,
        telefono: body.telefono || '',
        empresa: body.empresa || '',
        tipo_evento,
        descripcion,
        fecha_estimada: body.fecha_estimada || null,
        presupuesto_estimado: body.presupuesto_estimado || '',
        estado: 'nuevo',
      },
    ])
    .select()
    .single();

  if (error) return res.status(500).json({ error: error.message });

  // TODO: notificar al admin por email (Edge Function send-cotizacion-email aun no existe).

  res.status(201).json(data);
});
