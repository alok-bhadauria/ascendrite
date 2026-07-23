import React, { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { useLayoutStore } from '../../store/layoutStore';

export default function AppLayout() {
  const { sidebarOpen, setSidebarOpen, toggleCommandPalette } = useLayoutStore();

  // Listen to keyboard shortcut events
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Toggle Command Palette (Ctrl+K or Cmd+K)
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        toggleCommandPalette();
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="flex-1 flex w-full relative">
      {/* Dynamic Sidebar navigation */}
      <Sidebar />

      {/* Mobile background overlay */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 top-[73px] bg-black/40 z-20 lg:hidden animate-fade-in"
          aria-hidden="true"
        />
      )}

      {/* Primary content area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Outlet />
      </div>
    </div>
  );
}
