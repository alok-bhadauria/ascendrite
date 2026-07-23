import { create } from 'zustand';

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
  }
}));
