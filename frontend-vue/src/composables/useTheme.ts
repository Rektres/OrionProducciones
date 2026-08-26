import { ref } from 'vue';

export type Theme = 'dark' | 'light';

const THEME_KEY = 'orion_theme';

const theme = ref<Theme>((localStorage.getItem(THEME_KEY) as Theme | null) || 'light');

const aplicarTema = (t: Theme) => {
  document.documentElement.setAttribute('data-bs-theme', t);
  localStorage.setItem(THEME_KEY, t);
  theme.value = t;
};

// Se aplica apenas se importa este modulo (antes de montar la app en
// main.ts) para evitar un parpadeo del tema por defecto.
aplicarTema(theme.value);

export function useTheme() {
  const toggle = () => aplicarTema(theme.value === 'dark' ? 'light' : 'dark');
  return { theme, toggle };
}
