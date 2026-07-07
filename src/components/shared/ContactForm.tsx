import { useState } from 'react';
import { Button } from '@/components/ui';
import { contactoService } from '@/services/contacto.service';
import { CotizacionFormData } from '@/types';
import { motion } from 'framer-motion';

export const ContactForm = () => {
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState<CotizacionFormData>({
    nombre: '',
    email: '',
    telefono: '',
    empresa: '',
    tipo_evento: 'corporativo',
    descripcion: '',
    fecha_estimada: '',
    presupuesto_estimado: '',
  });

  const hoy = new Date().toISOString().split('T')[0];

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const cotizacion = await contactoService.crearCotizacion(formData);
      await contactoService.notificarAdminCotizacion(cotizacion.id);
      setSubmitted(true);

      setTimeout(() => {
        setSubmitted(false);
        setFormData({
          nombre: '',
          email: '',
          telefono: '',
          empresa: '',
          tipo_evento: 'corporativo',
          descripcion: '',
          fecha_estimada: '',
          presupuesto_estimado: '',
        });
      }, 5000);
    } catch (error) {
      console.error('Error enviando cotización:', error);
      alert('Error enviando la cotización. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-card border border-border rounded-lg p-8 text-center"
      >
        <h3 className="text-2xl font-bebas text-primary mb-4">Recibimos tu solicitud</h3>
        <p className="text-muted mb-6">
          Te contactaremos en menos de 24 horas. Mientras tanto, puedes escribirnos por WhatsApp
          si prefieres acelerar el proceso.
        </p>
        <a
          href={`https://wa.me/${import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378'}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:text-secondary transition-colors"
        >
          Contactar por WhatsApp
        </a>
      </motion.div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Nombre *</label>
          <input
            type="text"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors"
            placeholder="Tu nombre"
          />
        </div>

        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Email *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors"
            placeholder="tu@email.com"
          />
        </div>

        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Teléfono</label>
          <input
            type="tel"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors"
            placeholder="+56 9 1234 5678"
          />
        </div>

        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Empresa</label>
          <input
            type="text"
            name="empresa"
            value={formData.empresa}
            onChange={handleChange}
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors"
            placeholder="Tu empresa"
          />
        </div>

        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Tipo de Evento *</label>
          <select
            name="tipo_evento"
            value={formData.tipo_evento}
            onChange={handleChange}
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text focus:outline-none focus:border-primary transition-colors"
          >
            <option value="corporativo">Corporativo</option>
            <option value="social">Social</option>
            <option value="festival">Festival / Concierto</option>
            <option value="otro">Otro</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-grotesk text-text mb-2">Fecha Estimada</label>
          <input
            type="date"
            name="fecha_estimada"
            value={formData.fecha_estimada}
            onChange={handleChange}
            min={hoy}
            className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text focus:outline-none focus:border-primary transition-colors [color-scheme:dark]"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-grotesk text-text mb-2">Descripción del evento *</label>
        <textarea
          name="descripcion"
          value={formData.descripcion}
          onChange={handleChange}
          required
          rows={5}
          className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors resize-none"
          placeholder="Cuéntanos sobre tu evento, qué imaginas, presupuesto aproximado..."
        />
      </div>

      <div>
        <label className="block text-sm font-grotesk text-text mb-2">Presupuesto estimado</label>
        <input
          type="text"
          name="presupuesto_estimado"
          value={formData.presupuesto_estimado}
          onChange={handleChange}
          className="w-full bg-card border border-border rounded-lg px-4 py-2 text-text placeholder-muted focus:outline-none focus:border-primary transition-colors"
          placeholder="Ej: $500.000 - $1.000.000"
        />
      </div>

      <Button type="submit" disabled={loading} className="w-full">
        {loading ? 'Enviando...' : 'Enviar Cotización'}
      </Button>
    </form>
  );
};
