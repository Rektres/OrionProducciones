import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Menu, X, Zap } from 'lucide-react';
import { Button } from '@/components/ui';

const navLinks = [
  { label: 'Inicio', href: '/' },
  { label: 'Servicios', href: '/servicios' },
  { label: 'Portafolio', href: '/portafolio' },
  { label: 'Blog', href: '/blog' },
];

export const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      initial={{ backgroundColor: 'rgba(10, 10, 15, 0)' }}
      animate={{
        backgroundColor: isScrolled ? 'rgba(10, 10, 15, 0.95)' : 'rgba(10, 10, 15, 0)',
      }}
      className="fixed top-0 w-full z-50 border-b border-border/10"
      transition={{ duration: 0.3 }}
    >
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bebas text-2xl">
          <Zap className="text-primary" size={28} />
          <span className="text-primary">ORION</span>
        </Link>

        <div className="hidden md:flex gap-8 items-center">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className="text-text hover:text-primary transition-colors font-grotesk"
            >
              {link.label}
            </Link>
          ))}
          <Button onClick={() => navigate('/#cotizacion')}>
            Cotiza
          </Button>
        </div>

        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden text-primary"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden bg-card border-t border-border"
        >
          <div className="flex flex-col gap-4 px-4 py-6">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="text-text hover:text-primary transition-colors"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <Button
              className="w-full"
              onClick={() => {
                setIsOpen(false);
                navigate('/#cotizacion');
              }}
            >
              Cotiza
            </Button>
          </div>
        </motion.div>
      )}
    </motion.nav>
  );
};
