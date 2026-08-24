import datetime
from catalogo.models import (
    CategoriaServicio, Servicio, EventoTipo, Evento, FotoEvento, Tag, Post, PostTag
)

def run_seed():
    print("Iniciando seed de datos para Orion Stage (Pre-Produccion)...")

    # 1. CATEGORIAS DE SERVICIOS
    cats_data = [
        ("Audio & Sonido", "audio", 1),
        ("Iluminacion Escenica", "iluminacion", 2),
        ("Escenarios & Truss", "escenarios", 3),
        ("Pantallas & Visuales", "visuales", 4),
        ("Banqueteria & Ambientacion", "banqueteria", 5),
        ("Produccion Tecnica 360", "produccion", 6),
    ]
    cats = {}
    for nombre, slug, orden in cats_data:
        cat, _ = CategoriaServicio.objects.update_or_create(
            slug=slug,
            defaults={"nombre": nombre, "orden": orden}
        )
        cats[slug] = cat

    # 2. SERVICIOS
    servicios_data = [
        {
            "cat": "audio",
            "nombre": "Sonido Line Array Profesional",
            "desc_corta": "Sistemas de audio de alta fidelidad y potencia acustica para recintos abiertos y cerrados.",
            "desc_larga": "Provision e ingenieria de audio con sistemas Line Array de estandar internacional. Incluye consolas digitales de ultima generacion, microfonia inalambrica profesional UHF/Dante, monitoreo in-ear para artistas y calibracion acustica con ingenieros de sonido certificados.",
            "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",
            "orden": 1
        },
        {
            "cat": "iluminacion",
            "nombre": "Iluminacion Robotica & Show Laser",
            "desc_corta": "Cabezas moviles Beam/Spot/Wash, sistemas laser RGB y diseno de luces programado en consolas GrandMA.",
            "desc_larga": "Diseno de iluminacion arquitectonica y escenica de alto impacto. Contamos con cabezas moviles hibridas, barras LED pixel map, maquinas de humo criogenico y consolas DMX avanzadas para sincronizar la iluminacion con la musica y la narrativa del evento.",
            "img": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=1200&q=80",
            "orden": 2
        },
        {
            "cat": "escenarios",
            "nombre": "Escenarios Modulares & Estructuras Layher",
            "desc_corta": "Montaje de escenarios certificados, tarimas modulares antideslizantes y estructuras Truss de aluminio.",
            "desc_larga": "Infraestructura estructural completa para conciertos, festivales y galas. Estructuras Layher certificadas, techos ground support, torres de sonido, gradas y tarimas modulares ajustables en altura con barandas de seguridad y memoria de calculo de ingenieria.",
            "img": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=1200&q=80",
            "orden": 3
        },
        {
            "cat": "visuales",
            "nombre": "Pantallas LED Gigantes & Visual Mapping",
            "desc_corta": "Pantallas LED de alta resolucion indoor/outdoor P2.9 y P3.9 con servidores de medios y mapping.",
            "desc_larga": "Despliegue visual inmersivo con modulos LED de alto brillo y contraste, aptos para luz solar directa o recintos oscuros. Incluye switchers de video 4K, camaras de circuito cerrado para transmision en vivo y renderizado de visuales generativas.",
            "img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80",
            "orden": 4
        },
        {
            "cat": "banqueteria",
            "nombre": "Banqueteria & Cocteleria de Alta Gama",
            "desc_corta": "Servicio gastronomico gourmet, barras de autor y ambientacion personalizada para celebraciones y galas.",
            "desc_larga": "Experiencias gastronomicas de primer nivel con chefs profesionales. Menus de 3 y 4 tiempos, estaciones de cocteles de autor, estaciones tematicas y atencion de garzones y sommelier con mobiliario de lujo.",
            "img": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=1200&q=80",
            "orden": 5
        },
        {
            "cat": "produccion",
            "nombre": "Direccion Tecnica & Produccion 360°",
            "desc_corta": "Planificacion integral, coordinacion de proveedores, cronogramas minuciosos y regiduria de escenario.",
            "desc_larga": "Servicio de produccion ejecutiva de principio a fin. Nos encargamos de permisos, planos tecnicos 3D, coordinacion de artistas, staff de seguridad, generadores electricos redundantes y direccion minuto a minuto durante la jornada.",
            "img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80",
            "orden": 6
        },
    ]
    for s in servicios_data:
        cat = cats[s["cat"]]
        Servicio.objects.update_or_create(
            nombre=s["nombre"],
            defaults={
                "categoria": cat,
                "categoria_slug": cat.slug,
                "descripcion_corta": s["desc_corta"],
                "descripcion_larga": s["desc_larga"],
                "imagen": s["img"],
                "activo": True,
                "orden": s["orden"]
            }
        )

    # 3. TIPOS DE EVENTOS
    tipos_data = [
        ("Corporativo", "corporativo"),
        ("Festival", "festival"),
        ("Social & Bodas", "social"),
    ]
    tipos = {}
    for nombre, slug in tipos_data:
        t, _ = EventoTipo.objects.update_or_create(
            slug=slug,
            defaults={"nombre": nombre}
        )
        tipos[slug] = t

    # 4. EVENTOS
    eventos_data = [
        {
            "nombre": "Festival Sunset Electronic 2026",
            "slug": "festival-sunset-electronic-2026",
            "tipo": "festival",
            "cliente": "Producciones Sunset Chile",
            "lugar": "Espacio Riesco, Santiago",
            "asistentes": 4500,
            "desc_corta": "Produccion tecnica integral del escenario principal con sistema Line Array y 48 cabezas moviles.",
            "desc_larga": "Despliegue de un escenario de 18x12 metros con techo Layher, pantalla LED central de 10x4 metros y 2 laterales. Show de luces sincronizado por timecode y show de lasers de 20W.",
            "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",
            "destacado": True,
            "fotos": [
                ("https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=1200&q=80", "Efectos luminicos en escenario principal"),
                ("https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=1200&q=80", "Vista panoramica del publico y sonido Line Array"),
            ]
        },
        {
            "nombre": "Gala Anual Minera del Cobre",
            "slug": "gala-anual-minera-del-cobre",
            "tipo": "corporativo",
            "cliente": "Asociacion Nacional de Mineria",
            "lugar": "Hotel Sheraton, Santiago",
            "asistentes": 800,
            "desc_corta": "Cena de gala corporativa con sonido distribuido, pantallas de alta definicion y premiacion.",
            "desc_larga": "Ambientacion elegante con iluminacion perimetral en tonos cobrizos y dorados, microfonia inalambrica digital y transmision en streaming a mas de 5 paises.",
            "img": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=1200&q=80",
            "destacado": True,
            "fotos": [
                ("https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=1200&q=80", "Banqueteria y montaje de mesas de honor"),
                ("https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80", "Escenario principal de premiacion"),
            ]
        },
        {
            "nombre": "Lanzamiento Automotriz Quantum EV",
            "slug": "lanzamiento-automotriz-quantum-ev",
            "tipo": "corporativo",
            "cliente": "Quantum Motors Chile",
            "lugar": "Centro Parque, Las Condes",
            "asistentes": 650,
            "desc_corta": "Show de develacion de vehiculo electrico con visual mapping y show laser interactivo.",
            "desc_larga": "Produccion tecnica futurista con pasarela iluminada con barras pixel DMX, audio envolvente 7.1 y cabinas de demostracion interactiva para la prensa.",
            "img": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=1200&q=80",
            "destacado": True,
            "fotos": [
                ("https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80", "Develacion de prototipo con humo criogenico"),
            ]
        },
        {
            "nombre": "Matrimonio Premium Vina Santa Rita",
            "slug": "matrimonio-premium-vina-santa-rita",
            "tipo": "social",
            "cliente": "Familia Valenzuela Edwards",
            "lugar": "Vina Santa Rita, Buin",
            "asistentes": 320,
            "desc_corta": "Celebracion de matrimonio boutique con iluminacion arquitectonica en parque y carpa calefaccionada.",
            "desc_larga": "Instalacion de cielo estrellado con mas de 2000 micro-luces calidas, pista de baile de microcemento iluminada, audio envolvente para banda en vivo y DJ set.",
            "img": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80",
            "destacado": True,
            "fotos": [
                ("https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80", "Pista de baile y ambientacion luminica"),
            ]
        },
        {
            "nombre": "Concierto Acustico Arena Monticello",
            "slug": "concierto-acustico-arena-monticello",
            "tipo": "festival",
            "cliente": "Gran Arena Producciones",
            "lugar": "San Francisco de Mostazal",
            "asistentes": 3200,
            "desc_corta": "Show acustico intimo de gran escala con refuerzo de sonido Meyer Sound y luces calidas.",
            "desc_larga": "Ingenieria de sonido de ultra precision acustica para orquesta de cuerdas y banda en vivo, diseno de visuales teatrales sutiles y grabacion multipista en vivo.",
            "img": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=1200&q=80",
            "destacado": False,
            "fotos": [
                ("https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=1200&q=80", "Banda en vivo en Arena Monticello"),
            ]
        },
        {
            "nombre": "Congreso Internacional de Innovacion Tech",
            "slug": "congreso-internacional-innovacion-tech",
            "tipo": "corporativo",
            "cliente": "Fundacion Chile Futuro",
            "lugar": "CasaPiedra, Vitacura",
            "asistentes": 1500,
            "desc_corta": "3 dias de conferencias con 4 salas simultaneas de audio, streaming 4K y cabinas de traduccion.",
            "desc_larga": "Infraestructura tecnica para mas de 40 expositores internacionales, microfonia cuello de ganso con cancelacion de ruido, pantallas LED P2.5 y enlaces satelitales redundantes.",
            "img": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1200&q=80",
            "destacado": False,
            "fotos": [
                ("https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1200&q=80", "Plenaria principal del congreso"),
            ]
        },
    ]

    for ev_data in eventos_data:
        tipo = tipos[ev_data["tipo"]]
        evento, _ = Evento.objects.update_or_create(
            slug=ev_data["slug"],
            defaults={
                "nombre": ev_data["nombre"],
                "tipo": tipo,
                "tipo_slug": tipo.slug,
                "cliente": ev_data["cliente"],
                "lugar": ev_data["lugar"],
                "asistentes": ev_data["asistentes"],
                "descripcion_corta": ev_data["desc_corta"],
                "descripcion_larga": ev_data["desc_larga"],
                "imagen_destacada": ev_data["img"],
                "fecha_realizacion": datetime.date(2026, 1, 15),
                "destacado": ev_data["destacado"],
                "publicado": True,
                "orden": 1
            }
        )
        for idx, (f_img, f_desc) in enumerate(ev_data.get("fotos", [])):
            FotoEvento.objects.update_or_create(
                evento=evento,
                imagen=f_img,
                defaults={"descripcion": f_desc, "orden": idx}
            )

    # 5. PREGUNTAS FRECUENTES (FAQ / POSTS)
    tag_faq, _ = Tag.objects.update_or_create(slug="faq", defaults={"nombre": "FAQ"})

    faqs_data = [
        (
            "¿Con cuánta anticipación debo cotizar y reservar la fecha de mi evento?",
            "con-cuanta-anticipacion-cotizar",
            "Recomendamos cotizar con al menos 2 a 4 semanas de anticipacion para eventos corporativos y sociales, y entre 2 a 3 meses para festivales o eventos masivos. De esta forma aseguramos la disponibilidad de equipos especificos y realizamos la visita tecnica previa con tiempo.",
            "<p>Recomendamos cotizar con al menos <strong>2 a 4 semanas de anticipacion</strong> para eventos corporativos y sociales, y entre <strong>2 a 3 meses</strong> para festivales o eventos masivos de gran escala.</p><p>Esto nos permite realizar la visita tecnica al recinto, disenar los planos 3D de escenario y asegurar la reserva de equipamiento de audio Line Array y luminarias roboticas.</p>"
        ),
        (
            "¿Qué cobertura geográfica tienen dentro de Chile?",
            "cobertura-geografica-chile",
            "Contamos con flota logistica propia y realizamos producciones en todo el territorio chileno, desde Arica hasta Punta Arenas.",
            "<p>Nuestra base central de operaciones se encuentra en <strong>Santiago</strong>, pero contamos con logistica de transporte pesada para cubrir eventos en <strong>todo Chile</strong> (Valparaiso, Vina del Mar, Concepcion, La Serena, Antofagasta, Puerto Varas y mas).</p>"
        ),
        (
            "¿El servicio incluye personal técnico calificado y operadores durante el evento?",
            "personal-tecnico-operadores-incluidos",
            "Si, todos nuestros arriendos y servicios incluyen ingenieros de sonido, iluminadores DMX y operadores tecnicos certificados.",
            "<p>Absolutamente. En Orion Stage no solo proveemos equipamiento de vanguardia; cada montaje incluye un <strong>equipo humano profesional</strong>:</p><ul><li>Ingeniero de Sonido (FOH y Monitores)</li><li>Tecnico Iluminador y operador de consolas GrandMA</li><li>Director tecnico y asistentes de escenario (Roadies)</li></ul>"
        ),
        (
            "¿Cómo se realiza el proceso de pago y reserva de fecha?",
            "proceso-de-pago-y-reserva",
            "El proceso se formaliza mediante contrato con un 50% de anticipo al reservar y el saldo restante antes o el mismo dia del montaje.",
            "<p>Una vez aprobada la propuesta tecnica y comercial:</p><ol><li>Se emite el contrato de prestacion de servicios y orden de compra / factura.</li><li>Se realiza el pago de reserva del <strong>50% del total</strong>.</li><li>El <strong>50% restante</strong> se liquida hasta el dia previo o durante la prueba de sonido del evento.</li></ol><p>Aceptamos transferencias bancarias directas y pagos con tarjeta de credito corporativa.</p>"
        ),
        (
            "¿Cuentan con generadores eléctricos y respaldo para cortes de energía?",
            "generadores-electricos-respaldo-ups",
            "Si, ofrecemos grupos electrogenos insonorizados y sistemas de respaldo UPS para garantizar cero interrupciones en tu show.",
            "<p>Para eventos al aire libre o recintos de alto consumo, disponemos de <strong>grupos electrogenos insonorizados</strong> de 60 kVA a 250 kVA con certificacion SEC y tableros de distribucion trifasicos, ademas de sistemas UPS para consolas y servidores de video.</p>"
        ),
        (
            "¿Puedo solicitar una visita técnica previa al recinto del evento?",
            "visita-tecnica-previa-recinto",
            "Por supuesto. Coordinamos una visita tecnica con nuestro director de produccion para evaluar accesos, acustica y empalmes electricos.",
            "<p>Coordinamos visitas tecnicas en terreno para evaluar dimensiones de escenario, tiro de proyeccion de proyectores/LED, accesos de carga para camiones y capacidad de empalme electrico del recinto, asegurando un montaje sin imprevistos.</p>"
        ),
    ]

    for titulo, slug, extracto, contenido in faqs_data:
        post, _ = Post.objects.update_or_create(
            slug=slug,
            defaults={
                "titulo": titulo,
                "extracto": extracto,
                "contenido": contenido,
                "estado": "publicado",
                "fecha_publicacion": datetime.datetime.now(datetime.timezone.utc)
            }
        )
        PostTag.objects.get_or_create(post=post, tag=tag_faq)

    print(f"Seed completado exitosamente: {len(servicios_data)} servicios, {len(eventos_data)} eventos y {len(faqs_data)} FAQs ingresadas.")

if __name__ == "__main__":
    run_seed()
