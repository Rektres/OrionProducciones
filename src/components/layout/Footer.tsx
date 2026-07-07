import { Link } from 'react-router-dom';
import { MapPin, Phone } from 'lucide-react';

const WHATSAPP_NUMBER = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const WHATSAPP_URL = `https://wa.me/${WHATSAPP_NUMBER}`;

export const Footer = () => {
  return (
    <footer className="bg-surface border-t border-border mt-20">
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div>
            <h3 className="font-bebas text-2xl text-primary mb-4">ORION</h3>
            <p className="text-muted text-sm">
              Creamos experiencias inolvidables. Desde lo corporativo hasta lo más social,
              cada evento es una oportunidad para brillar.
            </p>
          </div>

          <div>
            <h4 className="font-grotesk font-semibold text-text mb-4">Sitio</h4>
            <ul className="space-y-2 text-sm text-muted">
              <li>
                <Link to="/" className="hover:text-primary transition-colors">
                  Inicio
                </Link>
              </li>
              <li>
                <Link to="/servicios" className="hover:text-primary transition-colors">
                  Servicios
                </Link>
              </li>
              <li>
                <Link to="/portafolio" className="hover:text-primary transition-colors">
                  Portafolio
                </Link>
              </li>
              <li>
                <Link to="/blog" className="hover:text-primary transition-colors">
                  Blog
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-grotesk font-semibold text-text mb-4">Contacto</h4>
            <ul className="space-y-3 text-sm text-muted">
              <li className="flex items-center gap-2">
                <Phone size={16} className="text-primary" />
                <a
                  href={WHATSAPP_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-primary transition-colors"
                >
                  +{WHATSAPP_NUMBER}
                </a>
              </li>
              <li className="flex items-center gap-2">
                <MapPin size={16} className="text-primary" />
                <span>Santiago, Chile</span>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-grotesk font-semibold text-text mb-4">Redes</h4>
            <ul className="space-y-2 text-sm text-muted">
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  Instagram
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  LinkedIn
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  Facebook
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border pt-8">
          <p className="text-center text-sm text-muted">
            © 2026 Todos los derechos reservados | Desarrollado por Mateo Araneda Medina
          </p>
        </div>
      </div>
    </footer>
  );
};
