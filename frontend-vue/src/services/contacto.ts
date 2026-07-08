import { api } from './api';
import type { CotizacionFormData } from '@/types';

export const contactoService = {
  async crearCotizacion(data: CotizacionFormData) {
    const { data: cotizacion } = await api.post('/cotizaciones/', data);
    return cotizacion;
  },
};
