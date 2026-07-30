export const userStorage = {
  // Generate namespaced key safely using user object/ID context
  getKey: (user, baseKey) => {
    if (!user || !user.id) return null;
    return `${baseKey}-${user.id}`;
  },

  // Safe JSON getter
  getItem: (user, baseKey, defaultValue = null) => {
    const key = userStorage.getKey(user, baseKey);
    if (!key) return defaultValue;
    try {
      const saved = localStorage.getItem(key);
      return saved !== null ? JSON.parse(saved) : defaultValue;
    } catch {
      return defaultValue;
    }
  },

  // Safe JSON setter
  setItem: (user, baseKey, value) => {
    const key = userStorage.getKey(user, baseKey);
    if (!key) return;
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      console.error(`Failed to write namespaced localStorage key "${key}":`, err);
    }
  },

  // Safe raw text getter
  getRawItem: (user, baseKey, defaultValue = '') => {
    const key = userStorage.getKey(user, baseKey);
    if (!key) return defaultValue;
    try {
      const saved = localStorage.getItem(key);
      return saved !== null ? saved : defaultValue;
    } catch {
      return defaultValue;
    }
  },

  // Safe raw text setter
  setRawItem: (user, baseKey, value) => {
    const key = userStorage.getKey(user, baseKey);
    if (!key) return;
    try {
      localStorage.setItem(key, value);
    } catch (err) {
      console.error(`Failed to write raw namespaced localStorage key "${key}":`, err);
    }
  }
};

