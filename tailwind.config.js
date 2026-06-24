/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#FF3D6B',
        secondary: '#FFB800',
        tertiary: '#6B2FFA',
        surface: '#0A0A0F',
        card: '#13131A',
        border: '#1E1E2E',
        text: '#F8F8FF',
        muted: '#8888AA',
      },
      fontFamily: {
        bebas: ['Bebas Neue', 'sans-serif'],
        grotesk: ['Space Grotesk', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
