import axios from 'axios';

export const TOKEN_KEY = 'orion_admin_token';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      // Se usa window.location en vez del router para evitar un ciclo de
      // imports (api.ts <- services/* <- views/* <- router/index.ts).
      if (window.location.pathname.startsWith('/admin')) {
        window.location.assign('/admin/login');
      }
    }
    return Promise.reject(error);
  },
);
