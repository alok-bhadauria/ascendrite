import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLayoutStore } from '../../store/layoutStore';
import { useAuthStore } from '../../store/authStore';
import { Search, Shield, PenTool, Cpu, BookOpen, Palette, Terminal } from 'lucide-react';

export default function CommandPalette() {
  const { commandPaletteOpen, setCommandPaletteOpen } = useLayoutStore();
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  // Compile list of operations the user can perform
  const baseItems = [
    { type: 'navigation', label: 'Go to Learning Paths', icon: BookOpen, action: () => navigate('/learn') },
    { type: 'navigation', label: 'Go to Workspace Sandbox', icon: Cpu, action: () => navigate('/workspace') },
    { type: 'navigation', label: 'Go to Account Settings', icon: Shield, action: () => navigate('/profile') },
  ];

  if (user?.role === 'Contributor' || user?.capabilities?.includes('knowledge:write') || user?.role === 'Admin') {
    baseItems.push({ type: 'navigation', label: 'Go to Creator Platform', icon: PenTool, action: () => navigate('/creator') });
  }
  if (user?.role === 'Admin' || user?.capabilities?.includes('system:admin')) {
    baseItems.push({ type: 'navigation', label: 'Go to Admin OS Panel', icon: Shield, action: () => navigate('/admin') });
  }

  // Theme changing commands
  const themeItems = [
    { type: 'theme', label: 'Apply Dracula Theme', icon: Palette, action: () => document.getElementById('theme-dracula')?.click() || localStorage.setItem('theme', 'dracula') },
    { type: 'theme', label: 'Apply Sepia Theme', icon: Palette, action: () => document.getElementById('theme-sepia')?.click() || localStorage.setItem('theme', 'sepia') },
    { type: 'theme', label: 'Apply Matrix Theme', icon: Palette, action: () => document.getElementById('theme-matrix')?.click() || localStorage.setItem('theme', 'matrix') },
    { type: 'theme', label: 'Apply Carbon Theme', icon: Palette, action: () => document.getElementById('theme-carbon')?.click() || localStorage.setItem('theme', 'carbon') },
    { type: 'theme', label: 'Apply Nord Light Theme', icon: Palette, action: () => document.getElementById('theme-nord')?.click() || localStorage.setItem('theme', 'nord') },
    { type: 'theme', label: 'Apply Milkshake Theme', icon: Palette, action: () => document.getElementById('theme-milkshake')?.click() || localStorage.setItem('theme', 'milkshake') }
  ];

  const allItems = [...baseItems, ...themeItems];
  const filtered = allItems.filter(item => 
    item.label.toLowerCase().includes(query.toLowerCase())
  );

  // Auto-focus input on open
  useEffect(() => {
    if (commandPaletteOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [commandPaletteOpen]);

  // Handle keyboard traversal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!commandPaletteOpen) return;
      
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % Math.max(1, filtered.length));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + filtered.length) % Math.max(1, filtered.length));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filtered[selectedIndex]) {
          filtered[selectedIndex].action();
          setCommandPaletteOpen(false);
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        setCommandPaletteOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen, filtered, selectedIndex]);

  if (!commandPaletteOpen) return null;

  return (
    <div 
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-start justify-center pt-[15vh] px-4 animate-fade-in pointer-events-auto"
      onClick={() => setCommandPaletteOpen(false)}
    >
      <div 
        className="w-full max-w-lg bg-theme-surface border border-theme-border rounded-2xl shadow-elevated overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Row */}
        <div className="flex items-center gap-3 px-4 border-b border-theme-border/60 py-3.5">
          <Search className="h-5 w-5 text-theme-subtle" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Type a command or route to navigate..."
            className="flex-1 bg-transparent text-sm text-theme-text border-0 outline-none focus:ring-0 placeholder:text-theme-subtle"
          />
          <span className="text-[10px] font-mono bg-theme-border/50 text-theme-subtle px-1.5 py-0.5 rounded border border-theme-border">ESC</span>
        </div>

        {/* Action Commands List */}
        <div className="max-h-[300px] overflow-y-auto p-2 flex flex-col gap-0.5">
          {filtered.length > 0 ? (
            filtered.map((item, idx) => (
              <button
                key={idx}
                onClick={() => {
                  item.action();
                  setCommandPaletteOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold text-left transition-colors cursor-pointer focus:outline-none ${
                  idx === selectedIndex 
                    ? 'bg-theme-border/55 text-theme-text' 
                    : 'text-theme-subtle hover:text-theme-text hover:bg-theme-border/20'
                }`}
              >
                <item.icon className="h-4 w-4 shrink-0" />
                <span className="flex-1">{item.label}</span>
                {idx === selectedIndex && (
                  <span className="text-[9px] font-mono opacity-80 flex items-center gap-0.5">
                    <Terminal className="h-3 w-3" />
                    <span>Enter</span>
                  </span>
                )}
              </button>
            ))
          ) : (
            <div className="text-center py-8">
              <p className="text-xs text-theme-subtle">No command outcomes matching "{query}" found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
