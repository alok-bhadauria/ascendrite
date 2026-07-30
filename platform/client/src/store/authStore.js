import { create } from 'zustand';
import api from '../utils/api';
import { userStorage } from '../utils/userStorage';

const getLocalPreferences = (userId) => {
  return userStorage.getItem({ id: userId }, 'ascendrite-preferences');
};

export const useAuthStore = create((set) => ({
  user: (() => {
    try {
      const savedUser = localStorage.getItem('ascendrite-user');
      if (!savedUser) return null;
      const u = JSON.parse(savedUser);
      const prefs = getLocalPreferences(u.id);
      if (prefs) {
        u.preferences = { ...u.preferences, ...prefs };
        u.onboarded = true;
      }
      return u;
    } catch {
      return null;
    }
  })(),
  isAuthenticated: !!localStorage.getItem('ascendrite-user'),
  isCheckingSession: true,
  
  login: (userData) => {
    // Update local preferences storage when user login data resolves
    if (userData && userData.id) {
      if (userData.preferences?.interest) {
        userStorage.setItem(userData, 'ascendrite-preferences', {
          interest: userData.preferences.interest,
          objective: userData.preferences.objective,
          onboarded: true
        });
      } else {
        const prefs = getLocalPreferences(userData.id);
        if (prefs) {
          userData.preferences = { ...userData.preferences, ...prefs };
          userData.onboarded = true;
        }
      }
    }
    localStorage.setItem('ascendrite-user', JSON.stringify(userData));
    set({ user: userData, isAuthenticated: true, isCheckingSession: false });
  },
  
  logout: () => {
    localStorage.removeItem('ascendrite-user');
    set({ user: null, isAuthenticated: false, isCheckingSession: false });
  },

  checkSession: async () => {
    try {
      const res = await api.get('/auth/me');
      const userData = res.data;
      const prefs = getLocalPreferences(userData.id);
      if (prefs) {
        userData.preferences = { ...userData.preferences, ...prefs };
        userData.onboarded = true;
      }
      localStorage.setItem('ascendrite-user', JSON.stringify(userData));
      set({ user: userData, isAuthenticated: true, isCheckingSession: false });
    } catch {
      localStorage.removeItem('ascendrite-user');
      set({ user: null, isAuthenticated: false, isCheckingSession: false });
    }
  }
}));

