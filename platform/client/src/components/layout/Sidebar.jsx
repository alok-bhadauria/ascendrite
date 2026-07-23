import React from 'react';
import { NavLink } from 'react-router-dom';
import { BookOpen, Cpu, PenTool, Users, Shield, Command } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useLayoutStore } from '../../store/layoutStore';

export default function Sidebar() {
  const { user } = useAuthStore();
  const { sidebarOpen, setSidebarOpen, toggleCommandPalette } = useLayoutStore();

  const handleLinkClick = () => {
    // Auto-close on mobile layouts
    if (window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  };

  // Compile navigation links dynamically based on user capabilities
  const mainLinks = [
    { to: '/learn', label: 'Learning Paths', icon: BookOpen },
    { to: '/workspace', label: 'Workspace Sandbox', icon: Cpu }
  ];

  const operationalLinks = [];
  if (user?.capabilities?.includes('creator:write') || user?.role === 'Admin') {
    operationalLinks.push({ to: '/creator', label: 'Creator platform', icon: PenTool });
  }
  if (user?.capabilities?.includes('collab:read') || user?.role === 'Admin') {
    operationalLinks.push({ to: '/collaboration', label: 'Collaboration', icon: Users });
  }
  if (user?.capabilities?.includes('admin:write') || user?.role === 'Admin') {
    operationalLinks.push({ to: '/admin', label: 'Admin OS', icon: Shield });
  }

  const baseLinkStyle = "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent";

  return (
    <aside
      className={`fixed lg:sticky top-[73px] left-0 h-[calc(100vh-73px)] w-64 bg-theme-surface border-r border-theme-border z-30 flex flex-col justify-between p-4 transition-transform duration-300 lg:transition-none ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:hidden'
      }`}
      aria-label="Sidebar Navigation"
    >
      <div className="flex flex-col gap-6">
        {/* Navigation block */}
        <div className="flex flex-col gap-1.5">
          <span className="px-4 text-[10px] font-bold text-theme-subtle/80 uppercase tracking-widest">
            Core Environment
          </span>
          {mainLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={handleLinkClick}
              className={({ isActive }) =>
                `${baseLinkStyle} ${
                  isActive 
                    ? 'bg-theme-bg text-theme-text shadow-sm' 
                    : 'text-theme-subtle hover:text-theme-text hover:bg-theme-border/20'
                }`
              }
            >
              <link.icon className="h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{link.label}</span>
            </NavLink>
          ))}
        </div>

        {/* Operational Modules block */}
        {operationalLinks.length > 0 && (
          <div className="flex flex-col gap-1.5">
            <span className="px-4 text-[10px] font-bold text-theme-subtle/80 uppercase tracking-widest">
              Operations Control
            </span>
            {operationalLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={handleLinkClick}
                className={({ isActive }) =>
                  `${baseLinkStyle} ${
                    isActive 
                      ? 'bg-theme-bg text-theme-text shadow-sm' 
                      : 'text-theme-subtle hover:text-theme-text hover:bg-theme-border/20'
                  }`
                }
              >
                <link.icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{link.label}</span>
              </NavLink>
            ))}
          </div>
        )}
      </div>

      {/* Footer shortcut blocks */}
      <div className="flex flex-col gap-2 pt-4 border-t border-theme-border">
        <button
          onClick={toggleCommandPalette}
          className="flex items-center justify-between w-full px-4 py-2.5 rounded-xl text-xs font-semibold text-theme-subtle hover:text-theme-text hover:bg-theme-border/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent cursor-pointer"
          aria-label="Open command palette"
        >
          <div className="flex items-center gap-2">
            <Command className="h-3.5 w-3.5" />
            <span>Command Palette</span>
          </div>
          <kbd className="px-1.5 py-0.5 text-[9px] bg-theme-bg border border-theme-border rounded">Ctrl K</kbd>
        </button>
      </div>
    </aside>
  );
}
