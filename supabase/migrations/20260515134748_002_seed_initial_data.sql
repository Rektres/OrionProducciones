/*
  # Seed Data - Productora Orion
  
  Inserta datos iniciales de ejemplo para desarrollo
*/

-- Categorías de Servicios
INSERT INTO categorias_servicio (nombre, slug, orden) VALUES
('Eventos Corporativos', 'corporativos', 1),
('Eventos Sociales', 'sociales', 2),
('Producción Técnica', 'produccion-tecnica', 3),
('Experiencias Inmersivas', 'experiencias-inmersivas', 4)
ON CONFLICT (slug) DO NOTHING;

-- Servicios
INSERT INTO servicios (categoria_id, categoria_slug, nombre, descripcion_corta, descripcion_larga, activo, orden) VALUES
((SELECT id FROM categorias_servicio WHERE slug = 'corporativos'), 'corporativos', 
 'Lanzamientos de Producto',
 'Presenta tus productos con impacto y profesionalismo',
 'Creamos experiencias de lanzamiento que generan buzz. Desde conceptualización hasta ejecución, manejamos cada detalle para que tu producto sea el centro de atención.',
 true, 1),
((SELECT id FROM categorias_servicio WHERE slug = 'corporativos'), 'corporativos',
 'Conferencias y Seminarios',
 'Eventos educativos con producción de clase mundial',
 'Organizamos conferencias que inspiran y educan. Manejo de espacios, sonido, proyección y moderación para máximo impacto.',
 true, 2),
((SELECT id FROM categorias_servicio WHERE slug = 'corporativos'), 'corporativos',
 'Teambuilding Corporativo',
 'Actividades que fortalecen equipos de trabajo',
 'Diseñamos experiencias divertidas y productivas que conectan a los equipos. Desde dinámicas simples hasta aventuras de varios días.',
 true, 3),
((SELECT id FROM categorias_servicio WHERE slug = 'sociales'), 'sociales',
 'Matrimonios y Celebraciones',
 'Tu día especial merece ser inolvidable',
 'Cada boda es única. Nos encargamos de la decoración, música, catering coordination y todos los detalles que hacen mágico tu día.',
 true, 4),
((SELECT id FROM categorias_servicio WHERE slug = 'sociales'), 'sociales',
 'Fiestas Temáticas',
 'Eventos con personalidad y ambiente único',
 'Transformamos espacios en universos temáticos. Desde la decoración hasta la experiencia sensorial completa.',
 true, 5),
((SELECT id FROM categorias_servicio WHERE slug = 'sociales'), 'sociales',
 'Graduaciones y Quinceañeros',
 'Celebra hitos de vida con estilo',
 'Creamos momentos memorables para estas ocasiones especiales. Producción completa con seguridad y atmosfera juvenil.',
 true, 6)
ON CONFLICT DO NOTHING;

-- Tipos de Eventos
INSERT INTO evento_tipos (nombre, slug) VALUES
('Corporativo', 'corporativo'),
('Social', 'social'),
('Festival', 'festival'),
('Concierto', 'concierto')
ON CONFLICT (slug) DO NOTHING;

-- Tags
INSERT INTO tags (nombre, slug) VALUES
('Producción', 'produccion'),
('Eventos', 'eventos'),
('Diseño', 'diseño'),
('Marketing', 'marketing'),
('Experiencia', 'experiencia'),
('Tendencias', 'tendencias')
ON CONFLICT (slug) DO NOTHING;

-- Eventos (Portafolio)
INSERT INTO eventos (nombre, slug, tipo_id, tipo_slug, cliente, descripcion_corta, descripcion_larga, imagen_destacada, fecha_realizacion, lugar, asistentes, destacado, publicado, orden) 
SELECT 
  'Lanzamiento Samsung Galaxy S25',
  'lanzamiento-samsung',
  id,
  'corporativo',
  'Samsung',
  'Experiencia futurista en Santiago',
  'Lanzamos el Galaxy S25 con una experiencia inmersiva que dejó a los asistentes sin aliento. Más de 500 personas vivieron el futuro de la tecnología móvil.',
  'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800',
  '2025-03-15'::date,
  'Centro de Convenciones Santiago',
  500,
  true,
  true,
  1
FROM evento_tipos WHERE slug = 'corporativo'
ON CONFLICT (slug) DO NOTHING;

INSERT INTO eventos (nombre, slug, tipo_id, tipo_slug, cliente, descripcion_corta, descripcion_larga, imagen_destacada, fecha_realizacion, lugar, asistentes, destacado, publicado, orden) 
SELECT 
  'Matrimonio Fernández & Rojas',
  'matrimonio-fernandez-rojas',
  id,
  'social',
  'Fernández - Rojas',
  'Una celebración de amor en la costa',
  'Una boda de ensueño en Viña del Mar con vistas al Pacífico. 200 invitados disfrutaron de gastronomía de clase mundial bajo las estrellas.',
  'https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&w=800',
  '2024-12-20'::date,
  'Viña del Mar, Valparaíso',
  200,
  true,
  true,
  2
FROM evento_tipos WHERE slug = 'social'
ON CONFLICT (slug) DO NOTHING;

INSERT INTO eventos (nombre, slug, tipo_id, tipo_slug, cliente, descripcion_corta, descripcion_larga, imagen_destacada, fecha_realizacion, lugar, asistentes, destacado, publicado, orden) 
SELECT 
  'TechSummit Chile 2024',
  'techsummit-2024',
  id,
  'corporativo',
  'TechSummit',
  'La conferencia de tecnología más grande del año',
  'Reunimos a 1000 innovadores, emprendedores y líderes tech en una jornada intensiva de networking, charlas magistrales y experiencias hands-on.',
  'https://images.pexels.com/photos/3808517/pexels-photo-3808517.jpeg?auto=compress&cs=tinysrgb&w=800',
  '2024-11-10'::date,
  'Espacio Riesco, Santiago',
  1000,
  true,
  true,
  3
FROM evento_tipos WHERE slug = 'corporativo'
ON CONFLICT (slug) DO NOTHING;

INSERT INTO eventos (nombre, slug, tipo_id, tipo_slug, cliente, descripcion_corta, descripcion_larga, imagen_destacada, fecha_realizacion, lugar, asistentes, destacado, publicado, orden) 
SELECT 
  'Fiesta de Graduación UDEC 2024',
  'graduacion-udec-2024',
  id,
  'social',
  'Universidad del Pacífico',
  'Celebración de la promoción 2024',
  'Más de 300 graduados celebraron su hito académico en una noche de pura energía. DJ en vivo, zona gaming y experiencias VR para todos.',
  'https://images.pexels.com/photos/2747446/pexels-photo-2747446.jpeg?auto=compress&cs=tinysrgb&w=800',
  '2024-12-05'::date,
  'Concepción',
  300,
  true,
  true,
  4
FROM evento_tipos WHERE slug = 'social'
ON CONFLICT (slug) DO NOTHING;

-- Posts del Blog
INSERT INTO posts (titulo, slug, imagen_destacada, extracto, contenido, estado, fecha_publicacion) VALUES
('Cómo planificar un evento corporativo sin morir en el intento',
 'como-planificar-evento-corporativo',
 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800',
 'Planificar un evento corporativo puede parecer abrumador. Aquí te compartimos los pasos clave para hacerlo como un profesional.',
 '<h2>Definir objetivos claros</h2><p>Antes de cualquier otra cosa, debes saber qué quieres lograr. ¿Networking? ¿Educación? ¿Diversión?</p><h2>Establece tu presupuesto</h2><p>Sé realista. Asigna fondos inteligentemente: 40% lugar, 30% catering, 20% AV/producción, 10% imprevistos.</p><h2>Timeline es todo</h2><p>Comienza 3 meses antes. Reserva lugar, proveedores y talentos con anticipación.</p>',
 'publicado',
 '2025-01-20'::timestamptz),
('Tendencias en decoración de matrimonios para 2025',
 'tendencias-decoracion-matrimonios-2025',
 'https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&w=800',
 'Este año los colores profundos y las texturas naturales dominan. Descubre qué hace que un matrimonio sea verdaderamente memorable.',
 '<h2>Colores intensos</h2><p>Olvida el rosa pálido. Los azul marino, borgoña y oro son los protagonistas.</p><h2>Sostenibilidad</h2><p>Las parejas modernas valoran decoraciones reutilizables y materiales ecológicos.</p><h2>Experiencia inmersiva</h2><p>La decoración debe contar una historia. Cada rincón es una oportunidad fotográfica.</p>',
 'publicado',
 '2025-02-05'::timestamptz),
('Por qué el sonido puede arruinar (o salvar) tu evento',
 'importancia-sonido-eventos',
 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=800',
 'Muchas productoras olvidan invertir en audio profesional. Un error que puede costar caro. Aquí te decimos por qué es crítico.',
 '<h2>Impacto emocional</h2><p>El sonido afecta emocionalmente. Música inadecuada mata la atmósfera en segundos.</p><h2>Claridad de mensaje</h2><p>Si los micrófonos fallan en una presentación, pierdes credibilidad y mensaje.</p><h2>Experiencia inmersiva</h2><p>El audio envolvente crea recuerdos duraderos. Invierte en equipamiento profesional.</p>',
 'publicado',
 '2025-02-10'::timestamptz)
ON CONFLICT (slug) DO NOTHING;

-- Relación post_tags
INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'como-planificar-evento-corporativo' AND t.slug = 'produccion'
ON CONFLICT (post_id, tag_id) DO NOTHING;

INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'como-planificar-evento-corporativo' AND t.slug = 'eventos'
ON CONFLICT (post_id, tag_id) DO NOTHING;

INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'tendencias-decoracion-matrimonios-2025' AND t.slug = 'tendencias'
ON CONFLICT (post_id, tag_id) DO NOTHING;

INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'tendencias-decoracion-matrimonios-2025' AND t.slug = 'diseño'
ON CONFLICT (post_id, tag_id) DO NOTHING;

INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'importancia-sonido-eventos' AND t.slug = 'produccion'
ON CONFLICT (post_id, tag_id) DO NOTHING;

INSERT INTO post_tags (post_id, tag_id) 
SELECT p.id, t.id FROM posts p, tags t 
WHERE p.slug = 'importancia-sonido-eventos' AND t.slug = 'experiencia'
ON CONFLICT (post_id, tag_id) DO NOTHING;
