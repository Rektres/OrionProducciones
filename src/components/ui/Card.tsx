import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: ReactNode;
  className?: string;
  hoverable?: boolean;
}

export const Card = ({
  children,
  className = '',
  hoverable = true,
}: CardProps) => {
  return (
    <motion.div
      whileHover={hoverable ? { scale: 1.02 } : {}}
      transition={{ duration: 0.3 }}
      className={`card-glass p-6 ${className}`}
    >
      {children}
    </motion.div>
  );
};
