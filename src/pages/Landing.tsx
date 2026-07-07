import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowDown } from 'lucide-react';
import { motion } from 'framer-motion';

import { Navbar, Footer, WhatsAppButton } from '@/components/layout';
import { ParticleBackground, FadeInUp, StaggerContainer } from '@/components/animations';
import { Button, Card, Badge } from '@/components/ui';
import { ContactForm } from '@/components/shared/ContactForm';

import { serviciosService } from '@/services/servicios.service';
import { portafolioService } from '@/services/portafolio.service';
import { blogService } from '@/services/blog.service';

import { Servicio, Evento, Post } from '@/types';

export const Landing = () => {
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [eventosDestacados, setEventosDestacados] = useState<Evento[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        const [svc, eventos, blog] = await Promise.all([
          serviciosService.getServicios(),
          portafolioService.getEventos(undefined, true),
          blogService.getPosts(3),
        ]);
        setServicios(svc);
        setEventosDestacados(eventos);
        setPosts(blog);
      } catch (error) {
        console.error('Error loading landing data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-12 h-12 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4"
          />
          <p className="text-muted">Cargando experiencia...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <WhatsAppButton />

      {/* Hero Section */}
      <section className="relative min-h-screen bg-surface pt-20 overflow-hidden flex items-center">
        <ParticleBackground />
        <div className="relative z-10 max-w-7xl mx-auto px-4 text-center py-32">
          <FadeInUp>
            <h1 className="text-5xl md:text-7xl font-bebas tracking-wider mb-6 text-text">
              CREAMOS EXPERIENCIAS
              <br />
              <span className="gradient-primary bg-clip-text text-transparent">
                INOLVIDABLES
              </span>
            </h1>
          </FadeInUp>

          <FadeInUp delay={0.2}>
            <p className="text-lg md:text-xl text-muted max-w-2xl mx-auto mb-12">
              Desde lo corporativo hasta lo más social. Cada evento es una oportunidad para brillar.
              Orion transforma tus ideas en realidad con producción de clase mundial.
            </p>
          </FadeInUp>

          <FadeInUp delay={0.4}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Button onClick={() => navigate('/portafolio')}>
                Ver Portafolio
              </Button>
              <Button
                variant="outline"
                onClick={() =>
                  document.querySelector('#cotizacion')?.scrollIntoView({ behavior: 'smooth' })
                }
              >
                Cotiza tu evento
              </Button>
            </div>
          </FadeInUp>

          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="mt-16"
          >
            <ArrowDown className="text-primary mx-auto" size={32} />
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-card/50 relative">
        <div className="max-w-7xl mx-auto px-4">
          <StaggerContainer>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { number: '+150', label: 'Eventos realizados' },
                { number: '+8', label: 'Años de experiencia' },
                { number: '+80', label: 'Clientes satisfechos' },
                { number: '+20', label: 'Ciudades alcanzadas' },
              ].map((stat, idx) => (
                <FadeInUp key={idx} delay={idx * 0.1}>
                  <div className="text-center">
                    <div className="relative">
                      <div className="text-6xl md:text-7xl font-bebas text-primary/10 absolute inset-0 flex items-center justify-center">
                        {stat.number}
                      </div>
                      <div className="text-4xl md:text-5xl font-bebas text-primary relative">
                        {stat.number}
                      </div>
                    </div>
                    <p className="text-muted mt-4 text-sm">{stat.label}</p>
                  </div>
                </FadeInUp>
              ))}
            </div>
          </StaggerContainer>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <h2 className="section-title text-center mb-16">LO QUE HACEMOS</h2>
          </FadeInUp>

          <StaggerContainer staggerDelay={0.05}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {servicios.slice(0, 6).map((servicio) => (
                <FadeInUp key={servicio.id}>
                  <Card>
                    <Badge variant="secondary" className="mb-4">
                      {servicio.nombre.split(' ')[0]}
                    </Badge>
                    <h3 className="text-xl font-grotesk font-bold text-text mb-3">
                      {servicio.nombre}
                    </h3>
                    <p className="text-sm text-muted leading-relaxed">
                      {servicio.descripcion_corta}
                    </p>
                  </Card>
                </FadeInUp>
              ))}
            </div>
          </StaggerContainer>
        </div>
      </section>

      {/* Portfolio Preview */}
      <section className="py-20 bg-card/50">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <h2 className="section-title text-center mb-16">NUESTRO TRABAJO</h2>
          </FadeInUp>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            {eventosDestacados.slice(0, 4).map((evento, idx) => (
              <FadeInUp key={evento.id} delay={idx * 0.1}>
                <Link to={`/portafolio/${evento.slug}`}>
                  <Card className="h-72 overflow-hidden group cursor-pointer">
                    <div
                      className="w-full h-full bg-cover bg-center relative group-hover:scale-105 transition-transform duration-300"
                      style={{
                        backgroundImage: `url('${evento.imagen_destacada}')`,
                      }}
                    >
                      <div className="gradient-overlay absolute inset-0 group-hover:opacity-50 transition-opacity duration-300 flex flex-col justify-end p-6">
                        <Badge variant="secondary" className="mb-3 w-fit">
                          {evento.tipo_id}
                        </Badge>
                        <h3 className="text-xl font-grotesk font-bold text-text">
                          {evento.nombre}
                        </h3>
                        <p className="text-sm text-muted mt-2">{evento.lugar}</p>
                      </div>
                    </div>
                  </Card>
                </Link>
              </FadeInUp>
            ))}
          </div>

          <div className="text-center">
            <Button onClick={() => navigate('/portafolio')} variant="outline">
              Ver todo el portafolio
            </Button>
          </div>
        </div>
      </section>

      {/* Blog Preview */}
      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <h2 className="section-title text-center mb-16">DESDE EL EQUIPO</h2>
          </FadeInUp>

          <StaggerContainer>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {posts.map((post, idx) => (
                <FadeInUp key={post.id} delay={idx * 0.1}>
                  <Link to={`/blog/${post.slug}`}>
                    <Card className="h-full overflow-hidden group cursor-pointer">
                      <div
                        className="w-full h-48 bg-cover bg-center mb-4 rounded group-hover:scale-110 transition-transform duration-300"
                        style={{
                          backgroundImage: `url('${post.imagen_destacada}')`,
                        }}
                      />
                      <Badge variant="primary" className="mb-3">
                        Blog
                      </Badge>
                      <h3 className="text-lg font-grotesk font-bold text-text mb-2">
                        {post.titulo}
                      </h3>
                      <p className="text-sm text-muted line-clamp-2">{post.extracto}</p>
                      <p className="text-xs text-muted mt-4">Leer más →</p>
                    </Card>
                  </Link>
                </FadeInUp>
              ))}
            </div>
          </StaggerContainer>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cotizacion" className="py-20 gradient-primary">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <FadeInUp>
            <h2 className="text-4xl md:text-6xl font-bebas text-white mb-6">
              ¿TIENES UN EVENTO EN MENTE?
            </h2>
          </FadeInUp>

          <FadeInUp delay={0.2}>
            <p className="text-lg text-white/90 mb-12">
              Cuéntanos tu idea y te contactamos en menos de 24 horas
            </p>
          </FadeInUp>

          <FadeInUp delay={0.4}>
            <ContactForm />
          </FadeInUp>
        </div>
      </section>

      <Footer />
    </>
  );
};
