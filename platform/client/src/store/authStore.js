import { create } from 'zustand';
import api from '../utils/api';

export const useAuthStore = create((set) => ({
  user: (() => {
    try {
      const savedUser = localStorage.getItem('ascendrite-user');
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  })(),
  isAuthenticated: !!localStorage.getItem('ascendrite-user'),
  
  login: (userData) => {
    localStorage.setItem('ascendrite-user', JSON.stringify(userData));
    set({ user: userData, isAuthenticated: true });
  },
  
  logout: () => {
    localStorage.removeItem('ascendrite-user');
    set({ user: null, isAuthenticated: false });
  },

  checkSession: async () => {
    try {
      const res = await api.get('/auth/me');
      localStorage.setItem('ascendrite-user', JSON.stringify(res.data));
      set({ user: res.data, isAuthenticated: true });
    } catch {
      localStorage.removeItem('ascendrite-user');
      set({ user: null, isAuthenticated: false });
    }
  }
}));
