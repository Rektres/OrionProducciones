import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import DOMPurify from 'dompurify';
import { Navbar, Footer, WhatsAppButton } from '@/components/layout';
import { FadeInUp, ParticleBackground } from '@/components/animations';
import { Card, Badge, Button } from '@/components/ui';
import { blogService } from '@/services/blog.service';
import { Post, Tag } from '@/types';

export const BlogLista = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const postsPerPage = 9;

  useEffect(() => {
    const loadData = async () => {
      try {
        const [postData, tagData] = await Promise.all([
          blogService.getPosts(postsPerPage, (page - 1) * postsPerPage),
          blogService.getTags(),
        ]);
        setPosts(postData);
        setTags(tagData);
      } catch (error) {
        console.error('Error loading blog:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [page]);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Cargando blog...</p>
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
              EL BLOG
            </h1>
          </FadeInUp>
          <FadeInUp delay={0.2}>
            <p className="text-lg text-muted">
              Consejos, tendencias e insights desde el equipo Orion
            </p>
          </FadeInUp>
        </div>
      </section>

      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4">
          <FadeInUp>
            <div className="flex flex-wrap gap-2 justify-center mb-16">
              <button
                onClick={() => setSelectedTag(null)}
                className={`px-4 py-2 rounded-full font-grotesk text-sm transition-all ${
                  selectedTag === null
                    ? 'gradient-primary text-white'
                    : 'bg-card text-text hover:border-primary border border-border'
                }`}
              >
                Todos
              </button>
              {tags.map((tag) => (
                <button
                  key={tag.id}
                  onClick={() => setSelectedTag(tag.slug)}
                  className={`px-4 py-2 rounded-full font-grotesk text-sm transition-all ${
                    selectedTag === tag.slug
                      ? 'gradient-primary text-white'
                      : 'bg-card text-text hover:border-primary border border-border'
                  }`}
                >
                  {tag.nombre}
                </button>
              ))}
            </div>
          </FadeInUp>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {posts.map((post) => (
              <FadeInUp key={post.id}>
                <Link to={`/blog/${post.slug}`}>
                  <Card className="h-full overflow-hidden cursor-pointer group">
                    <div
                      className="w-full h-48 bg-cover bg-center mb-4 rounded group-hover:scale-110 transition-transform duration-300"
                      style={{
                        backgroundImage: `url('${post.imagen_destacada}')`,
                      }}
                    />
                    <Badge variant="primary" className="mb-3">
                      Artículo
                    </Badge>
                    <h3 className="text-lg font-grotesk font-bold text-text mb-2">
                      {post.titulo}
                    </h3>
                    <p className="text-sm text-muted line-clamp-2 mb-4">{post.extracto}</p>
                    {post.tags && post.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {post.tags.slice(0, 2).map((tag) => (
                          <Badge key={tag.id} variant="secondary" className="text-xs">
                            {tag.nombre}
                          </Badge>
                        ))}
                      </div>
                    )}
                    <p className="text-xs text-primary hover:text-secondary transition-colors">
                      Leer más →
                    </p>
                  </Card>
                </Link>
              </FadeInUp>
            ))}
          </div>

          <div className="flex gap-4 justify-center mt-16">
            {page > 1 && (
              <Button variant="outline" onClick={() => setPage(page - 1)}>
                Anterior
              </Button>
            )}
            <Button variant="outline" onClick={() => setPage(page + 1)}>
              Siguiente
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
};

export const BlogDetalle = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPost = async () => {
      if (!slug) return;
      try {
        const data = await blogService.getPostBySlug(slug);
        setPost(data);
      } catch (error) {
        console.error('Error loading post:', error);
      } finally {
        setLoading(false);
      }
    };

    loadPost();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Cargando artículo...</p>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen bg-surface flex items-center justify-center">
        <p className="text-muted">Artículo no encontrado</p>
      </div>
    );
  }

  const cleanHtml = DOMPurify.sanitize(post.contenido);

  return (
    <>
      <Navbar />
      <WhatsAppButton />

      <section className="relative h-96 overflow-hidden">
        <div
          className="w-full h-full bg-cover bg-center"
          style={{
            backgroundImage: `url('${post.imagen_destacada}')`,
          }}
        >
          <div className="gradient-overlay absolute inset-0 flex flex-col justify-end p-8">
            <h1 className="text-4xl md:text-5xl font-bebas text-white">{post.titulo}</h1>
          </div>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-4 py-16">
        <div className="flex flex-wrap gap-3 mb-8">
          {post.tags?.map((tag) => (
            <Badge key={tag.id} variant="secondary">
              {tag.nombre}
            </Badge>
          ))}
        </div>

        <article
          className="prose prose-invert max-w-none mb-16"
          dangerouslySetInnerHTML={{ __html: cleanHtml }}
        />

        <div className="bg-card border border-border rounded-lg p-8 text-center">
          <h3 className="text-2xl font-bebas text-primary mb-4">¿Interesado en trabajar juntos?</h3>
          <p className="text-muted mb-6">Cuéntanos tu idea y haremos magia</p>
          <Button onClick={() => navigate('/#cotizacion')}>
            Solicitar cotización
          </Button>
        </div>
      </div>

      <Footer />
    </>
  );
};
