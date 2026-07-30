import { create } from 'zustand';

export const useLayoutStore = create((set) => ({
  // Default sidebar state resolves dynamically based on viewport dimensions
  sidebarOpen: window.innerWidth >= 1024,
  commandPaletteOpen: false,
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  
  toggleCommandPalette: () => set((state) => ({ commandPaletteOpen: !state.commandPaletteOpen })),
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open })
}));

