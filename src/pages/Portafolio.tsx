import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Navbar, Footer, WhatsAppButton } from '@/components/layout';
import { FadeInUp, ParticleBackground } from '@/components/animations';
import { Button, Card, Badge } from '@/components/ui';
import { ContactForm } from '@/components/shared/ContactForm';
import { portafolioService } from '@/services/portafolio.service';
import { Evento, EventoTipo } from '@/types';
import Masonry from 'react-masonry-css';

export const PortafolioLista = () => {
  const [tipos, setTipos] = useState<EventoTipo[]>([]);
  const [eventos, setEventos] = useState<Evento[]>([]);
  const [selectedTipo, setSelectedTipo] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [tipos, eventos] = await Promise.all([
          portafolioService.getTipos(),
          portafolioService.getEventos(),
        ]);
        setTipos(tipos);
        setEventos(eventos);
      } catch (error) {
        console.error('Error loading portafolio:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const filteredEventos = selectedTipo
    ? eventos.filter((e) => e.tipo_slug === selectedTipo)
    : eventos;

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Cargando portafolio...</p>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <WhatsAppButton />

      <section className="relative pt-32 pb-20 bg-surface overflow-hidden">
        <ParticleBackground />
        <div className="relative z-10 max-w-7xl mx-auto px-4 text-center">
          <FadeInUp>
            <h1 className="text-5xl md:text-7xl font-bebas tracking-wider mb-6 text-text">
              PORTAFOLIO
            </h1>
          </FadeInUp>
          <FadeInUp delay={0.2}>
            <p className="text-lg text-muted">
              {eventos.length} eventos realizados con pasión
            </p>
          </FadeInUp>
        </div>
      </section>

      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <div className="flex flex-wrap gap-3 justify-center mb-16">
              <button
                onClick={() => setSelectedTipo(null)}
                className={`px-6 py-2 rounded-full font-grotesk transition-all ${
                  selectedTipo === null
                    ? 'gradient-primary text-white'
                    : 'bg-card text-text hover:border-primary border border-border'
                }`}
              >
                Todos
              </button>
              {tipos.map((tipo) => (
                <button
                  key={tipo.id}
                  onClick={() => setSelectedTipo(tipo.slug)}
                  className={`px-6 py-2 rounded-full font-grotesk transition-all ${
                    selectedTipo === tipo.slug
                      ? 'gradient-primary text-white'
                      : 'bg-card text-text hover:border-primary border border-border'
                  }`}
                >
                  {tipo.nombre}
                </button>
              ))}
            </div>
          </FadeInUp>

          <Masonry
            breakpointCols={{ default: 3, 1024: 2, 640: 1 }}
            className="masonry-grid"
            columnClassName="masonry-grid-column"
          >
            {filteredEventos.map((evento) => (
              <FadeInUp key={evento.id}>
                <a href={`/portafolio/${evento.slug}`}>
                  <Card className="overflow-hidden cursor-pointer h-64">
                    <div
                      className="w-full h-full bg-cover bg-center relative group-hover:scale-105 transition-transform"
                      style={{
                        backgroundImage: `url('${evento.imagen_destacada}')`,
                      }}
                    >
                      <div className="gradient-overlay absolute inset-0 flex flex-col justify-end p-4">
                        <Badge variant="secondary">{evento.tipo_slug}</Badge>
                        <h3 className="text-lg font-grotesk font-bold text-text mt-2">
                          {evento.nombre}
                        </h3>
                        <p className="text-xs text-muted">{evento.lugar}</p>
                      </div>
                    </div>
                  </Card>
                </a>
              </FadeInUp>
            ))}
          </Masonry>
        </div>
      </section>

      <Footer />
    </>
  );
};

export const PortafolioDetalle = () => {
  const { slug } = useParams<{ slug: string }>();
  const [evento, setEvento] = useState<Evento | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadEvento = async () => {
      if (!slug) return;
      try {
        const data = await portafolioService.getEventoBySlug(slug);
        setEvento(data);
      } catch (error) {
        console.error('Error loading evento:', error);
      } finally {
        setLoading(false);
      }
    };

    loadEvento();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Cargando evento...</p>
      </div>
    );
  }

  if (!evento) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Evento no encontrado</p>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <WhatsAppButton />

      <section className="relative h-96 overflow-hidden">
        <div
          className="w-full h-full bg-cover bg-center"
          style={{
            backgroundImage: `url('${evento.imagen_destacada}')`,
          }}
        >
          <div className="gradient-overlay absolute inset-0 flex flex-col justify-end p-8">
            <Badge variant="secondary" className="w-fit mb-4">
              {evento.tipo_slug}
            </Badge>
            <h1 className="text-5xl font-bebas text-white">{evento.nombre}</h1>
          </div>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <Card>
            <h3 className="font-grotesk font-bold text-primary mb-2">Cliente</h3>
            <p className="text-text">{evento.cliente}</p>
          </Card>
          <Card>
            <h3 className="font-grotesk font-bold text-primary mb-2">Ubicación</h3>
            <p className="text-text">{evento.lugar}</p>
          </Card>
          <Card>
            <h3 className="font-grotesk font-bold text-primary mb-2">Asistentes</h3>
            <p className="text-text">{evento.asistentes ? `${evento.asistentes}+` : 'N/A'}</p>
          </Card>
        </div>

        <FadeInUp>
          <div className="mb-16">
            <h2 className="text-3xl font-bebas mb-6 text-primary">Sobre el evento</h2>
            <p className="text-muted leading-relaxed text-lg">{evento.descripcion_larga}</p>
          </div>
        </FadeInUp>

        {evento.fotos && evento.fotos.length > 0 && (
          <FadeInUp delay={0.2}>
            <div className="mb-16">
              <h2 className="text-3xl font-bebas mb-6 text-primary">Galería</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {evento.fotos.map((foto) => (
                  <a key={foto.id} href={foto.imagen} target="_blank" rel="noopener noreferrer">
                    <Card className="h-48 overflow-hidden cursor-pointer hover:opacity-80 transition">
                      <div
                        className="w-full h-full bg-cover bg-center"
                        style={{ backgroundImage: `url('${foto.imagen}')` }}
                      />
                    </Card>
                  </a>
                ))}
              </div>
            </div>
          </FadeInUp>
        )}

        <FadeInUp delay={0.4}>
          <div className="bg-card border border-border rounded-lg p-8 text-center">
            <h3 className="text-2xl font-bebas text-primary mb-4">¿Quieres un evento así?</h3>
            <p className="text-muted mb-6">Cuéntanos tu idea y crearemos algo especial</p>
            <Button onClick={() => window.location.href = '/#cotizacion'}>
              Solicitar cotización
            </Button>
          </div>
        </FadeInUp>
      </div>

      <Footer />
    </>
  );
};
