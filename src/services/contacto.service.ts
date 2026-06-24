import { supabase } from '@/lib/supabase';
import { Cotizacion, CotizacionFormData } from '@/types';

export const contactoService = {
  async crearCotizacion(data: CotizacionFormData): Promise<Cotizacion> {
    const { data: cotizacion, error } = await supabase
      .from('cotizaciones')
      .insert([
        {
          nombre: data.nombre,
          email: data.email,
          telefono: data.telefono || '',
          empresa: data.empresa || '',
          tipo_evento: data.tipo_evento,
          descripcion: data.descripcion,
          fecha_estimada: data.fecha_estimada || null,
          presupuesto_estimado: data.presupuesto_estimado || '',
          estado: 'nuevo',
        },
      ])
      .select()
      .single();

    if (error) throw error;
    return cotizacion;
  },

  async notificarAdminCotizacion(cotizacionId: string): Promise<void> {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/send-cotizacion-email`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
          },
          body: JSON.stringify({ cotizacionId }),
        }
      );

      if (!response.ok) {
        throw new Error('Error enviando notificación');
      }
    } catch (error) {
      console.error('Error notificando admin:', error);
    }
  },
};
