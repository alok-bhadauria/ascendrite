import { create } from 'zustand';
import api from '../utils/api';

const getLocalPreferences = (userId) => {
  if (!userId) return null;
  try {
    const saved = localStorage.getItem(`ascendrite-preferences-${userId}`);
    return saved ? JSON.parse(saved) : null;
  } catch {
    return null;
  }
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
    if (userData && userData.id) {
      // If the incoming user data already has onboarding preferences (or if we merge them)
      if (userData.preferences?.interest) {
        localStorage.setItem(
          `ascendrite-preferences-${userData.id}`,
          JSON.stringify({
            interest: userData.preferences.interest,
            objective: userData.preferences.objective,
            onboarded: true
          })
        );
      } else {
        // Retrieve existing preferences for this user if they exist in localStorage
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
