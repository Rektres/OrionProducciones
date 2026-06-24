/*
  # Productora Orion - Schema Inicial
  
  1. New Tables
    - `categorias_servicio` - Categorías de servicios (Corporativos, Sociales, etc.)
    - `servicios` - Servicios ofrecidos
    - `evento_tipos` - Tipos de eventos (Corporativo, Social, Festival)
    - `eventos` - Eventos del portafolio
    - `fotos_evento` - Galería de fotos por evento
    - `tags` - Etiquetas para blog posts
    - `posts` - Artículos del blog
    - `post_tags` - Relación posts con tags
    - `cotizaciones` - Solicitudes de cotización
  
  2. Security
    - Enable RLS on all tables
    - Public read access for published content
    - No write access for public users
    - Cotizaciones can be created by anyone but read only by admin
  
  3. Important Notes
    - All dates use timestamptz for consistency
    - slug fields must be unique and lowercase
    - orden field for manual ordering
    - All published/active content is public, drafts/inactive are private
*/

-- Categorías de Servicios
CREATE TABLE IF NOT EXISTS categorias_servicio (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  slug text UNIQUE NOT NULL,
  orden integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Servicios
CREATE TABLE IF NOT EXISTS servicios (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  categoria_id uuid REFERENCES categorias_servicio(id) ON DELETE SET NULL,
  categoria_slug text,
  nombre text NOT NULL,
  descripcion_corta text NOT NULL,
  descripcion_larga text NOT NULL,
  imagen text,
  icono_svg text,
  activo boolean DEFAULT true,
  orden integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Tipos de Eventos
CREATE TABLE IF NOT EXISTS evento_tipos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  slug text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Eventos (Portafolio)
CREATE TABLE IF NOT EXISTS eventos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  slug text UNIQUE NOT NULL,
  tipo_id uuid REFERENCES evento_tipos(id) ON DELETE SET NULL,
  tipo_slug text,
  cliente text NOT NULL,
  descripcion_corta text NOT NULL,
  descripcion_larga text NOT NULL,
  imagen_destacada text,
  fecha_realizacion date NOT NULL,
  lugar text NOT NULL,
  asistentes integer,
  destacado boolean DEFAULT false,
  publicado boolean DEFAULT true,
  orden integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Fotos de Eventos
CREATE TABLE IF NOT EXISTS fotos_evento (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  evento_id uuid REFERENCES eventos(id) ON DELETE CASCADE NOT NULL,
  imagen text NOT NULL,
  descripcion text,
  orden integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Tags para Blog
CREATE TABLE IF NOT EXISTS tags (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  slug text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Posts del Blog
CREATE TABLE IF NOT EXISTS posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  titulo text NOT NULL,
  slug text UNIQUE NOT NULL,
  imagen_destacada text,
  extracto text NOT NULL,
  contenido text NOT NULL,
  estado text DEFAULT 'borrador' CHECK (estado IN ('borrador', 'revision', 'publicado')),
  fecha_publicacion timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Relación Posts con Tags
CREATE TABLE IF NOT EXISTS post_tags (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id uuid REFERENCES posts(id) ON DELETE CASCADE NOT NULL,
  tag_id uuid REFERENCES tags(id) ON DELETE CASCADE NOT NULL,
  created_at timestamptz DEFAULT now(),
  UNIQUE(post_id, tag_id)
);

-- Cotizaciones
CREATE TABLE IF NOT EXISTS cotizaciones (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  email text NOT NULL,
  telefono text,
  empresa text,
  tipo_evento text NOT NULL CHECK (tipo_evento IN ('corporativo', 'social', 'festival', 'otro')),
  descripcion text NOT NULL,
  fecha_estimada date,
  presupuesto_estimado text,
  estado text DEFAULT 'nuevo' CHECK (estado IN ('nuevo', 'en_contacto', 'cotizado', 'cerrado', 'descartado')),
  created_at timestamptz DEFAULT now()
);

-- RLS Policies
ALTER TABLE categorias_servicio ENABLE ROW LEVEL SECURITY;
ALTER TABLE servicios ENABLE ROW LEVEL SECURITY;
ALTER TABLE evento_tipos ENABLE ROW LEVEL SECURITY;
ALTER TABLE eventos ENABLE ROW LEVEL SECURITY;
ALTER TABLE fotos_evento ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE post_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE cotizaciones ENABLE ROW LEVEL SECURITY;

-- Public read policies for categorias
CREATE POLICY "Categorías públicas de lectura"
  ON categorias_servicio FOR SELECT
  TO anon, authenticated
  USING (true);

-- Public read policies for servicios activos
CREATE POLICY "Servicios activos son públicos"
  ON servicios FOR SELECT
  TO anon, authenticated
  USING (activo = true);

-- Public read policies for evento_tipos
CREATE POLICY "Tipos de eventos públicos"
  ON evento_tipos FOR SELECT
  TO anon, authenticated
  USING (true);

-- Public read policies for eventos publicados
CREATE POLICY "Eventos publicados son públicos"
  ON eventos FOR SELECT
  TO anon, authenticated
  USING (publicado = true);

-- Public read policies for fotos
CREATE POLICY "Fotos de eventos publicados son públicas"
  ON fotos_evento FOR SELECT
  TO anon, authenticated
  USING (
    EXISTS (
      SELECT 1 FROM eventos WHERE eventos.id = fotos_evento.evento_id AND eventos.publicado = true
    )
  );

-- Public read for tags
CREATE POLICY "Tags públicos"
  ON tags FOR SELECT
  TO anon, authenticated
  USING (true);

-- Public read for published posts
CREATE POLICY "Posts publicados son públicos"
  ON posts FOR SELECT
  TO anon, authenticated
  USING (estado = 'publicado' AND fecha_publicacion IS NOT NULL);

-- Public read for post_tags of published posts
CREATE POLICY "Tags de posts publicados son públicos"
  ON post_tags FOR SELECT
  TO anon, authenticated
  USING (
    EXISTS (
      SELECT 1 FROM posts WHERE posts.id = post_tags.post_id AND posts.estado = 'publicado'
    )
  );

-- Public insert for cotizaciones
CREATE POLICY "Cualquiera puede crear cotizaciones"
  ON cotizaciones FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Indexes para performance
CREATE INDEX idx_servicios_categoria ON servicios(categoria_id);
CREATE INDEX idx_servicios_activo ON servicios(activo);
CREATE INDEX idx_eventos_tipo ON eventos(tipo_id);
CREATE INDEX idx_eventos_publicado ON eventos(publicado);
CREATE INDEX idx_eventos_fecha ON eventos(fecha_realizacion DESC);
CREATE INDEX idx_fotos_evento ON fotos_evento(evento_id);
CREATE INDEX idx_posts_estado ON posts(estado);
CREATE INDEX idx_posts_fecha ON posts(fecha_publicacion DESC);
CREATE INDEX idx_post_tags_post ON post_tags(post_id);
CREATE INDEX idx_post_tags_tag ON post_tags(tag_id);
