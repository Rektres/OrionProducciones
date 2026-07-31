import { api, TOKEN_KEY } from './api';

export const adminAuth = {
  async login(username: string, password: string): Promise<void> {
    const { data } = await api.post<{ token: string }>('/auth/token/', { username, password });
    localStorage.setItem(TOKEN_KEY, data.token);
  },

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem(TOKEN_KEY);
  },
};
