import { useEffect, useState } from 'react';
import { Navbar, Footer, WhatsAppButton } from '@/components/layout';
import { FadeInUp, StaggerContainer, ParticleBackground } from '@/components/animations';
import { Button, Card, Badge } from '@/components/ui';
import { ContactForm } from '@/components/shared/ContactForm';
import { serviciosService } from '@/services/servicios.service';
import { Servicio, CategoriaServicio } from '@/types';

export const Servicios = () => {
  const [categorias, setCategorias] = useState<CategoriaServicio[]>([]);
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [selectedCategoria, setSelectedCategoria] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [cats, svc] = await Promise.all([
          serviciosService.getCategorias(),
          serviciosService.getServicios(),
        ]);
        setCategorias(cats);
        setServicios(svc);
        if (cats.length > 0) setSelectedCategoria(cats[0].slug);
      } catch (error) {
        console.error('Error loading servicios:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const filteredServicios = selectedCategoria
    ? servicios.filter((s) => s.categoria_slug === selectedCategoria)
    : servicios;

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Cargando servicios...</p>
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
              NUESTROS
              <br />
              <span className="gradient-primary bg-clip-text text-transparent">SERVICIOS</span>
            </h1>
          </FadeInUp>
          <FadeInUp delay={0.2}>
            <p className="text-lg text-muted max-w-2xl mx-auto">
              Soluciones completas de producción para eventos de cualquier escala
            </p>
          </FadeInUp>
        </div>
      </section>

      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <div className="flex flex-wrap gap-3 justify-center mb-16">
              {categorias.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategoria(cat.slug)}
                  className={`px-6 py-2 rounded-full font-grotesk transition-all duration-300 ${
                    selectedCategoria === cat.slug
                      ? 'gradient-primary text-white'
                      : 'bg-card text-text hover:border-primary border border-border'
                  }`}
                >
                  {cat.nombre}
                </button>
              ))}
            </div>
          </FadeInUp>

          <StaggerContainer>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {filteredServicios.map((servicio, idx) => (
                <FadeInUp key={servicio.id} delay={idx * 0.05}>
                  <Card>
                    <Badge variant="secondary" className="mb-4">
                      {servicio.nombre}
                    </Badge>
                    <h3 className="text-2xl font-bebas text-primary mb-4">
                      {servicio.nombre}
                    </h3>
                    <p className="text-muted mb-6 leading-relaxed">
                      {servicio.descripcion_larga}
                    </p>
                    <Button
                      variant="outline"
                      onClick={() =>
                        document.querySelector('#cotizacion-servicios')?.scrollIntoView({
                          behavior: 'smooth',
                        })
                      }
                    >
                      Cotizar este servicio
                    </Button>
                  </Card>
                </FadeInUp>
              ))}
            </div>
          </StaggerContainer>
        </div>
      </section>

      <section id="cotizacion-servicios" className="py-20 gradient-primary">
        <div className="max-w-4xl mx-auto px-4">
          <FadeInUp>
            <h2 className="text-4xl font-bebas text-white mb-6 text-center">
              CUÉNTANOS TU IDEA
            </h2>
          </FadeInUp>
          <FadeInUp delay={0.2}>
            <ContactForm />
          </FadeInUp>
        </div>
      </section>

      <Footer />
    </>
  );
};
