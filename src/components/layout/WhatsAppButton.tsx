import { MessageCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const WHATSAPP_NUMBER = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
const WHATSAPP_URL = `https://wa.me/${WHATSAPP_NUMBER}`;

export const WhatsAppButton = () => {
  return (
    <motion.a
      href={WHATSAPP_URL}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-8 right-8 z-40 bg-gradient-primary text-white rounded-full p-4 shadow-lg shadow-primary/50"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      animate={{ scale: [1, 1.1, 1] }}
      transition={{
        duration: 2,
        repeat: Infinity,
        repeatType: 'loop',
      }}
      title="Cotiza por WhatsApp"
    >
      <MessageCircle size={28} />
    </motion.a>
  );
};
