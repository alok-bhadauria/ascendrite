import React, { useState, useEffect } from 'react';
import { FaPalette, FaGoogle } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const themes = [
  { id: 'carbon', name: 'Carbon (Dark)' },
  { id: 'dracula', name: 'Dracula (Dark)' },
  { id: 'matrix', name: 'Matrix (Dark)' },
  { id: 'nord-light', name: 'Nord Light (Light)' },
  { id: 'sepia', name: 'Sepia (Light)' },
  { id: 'milkshake', name: 'Milkshake (Light)' }
];

export default function Navbar() {
  const [activeTheme, setActiveTheme] = useState('carbon');
  const [showThemeDropdown, setShowThemeDropdown] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('ascendrite-theme') || 'carbon';
    setActiveTheme(savedTheme);
  }, []);

  const changeTheme = (themeId) => {
    localStorage.setItem('ascendrite-theme', themeId);
    document.documentElement.setAttribute('data-theme', themeId);
    setActiveTheme(themeId);
    setShowThemeDropdown(false);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-theme-bg bg-opacity-80 backdrop-blur-md border-b border-theme-border transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2 select-none">
          <div className="w-8 h-8 rounded-lg bg-theme-accent flex items-center justify-center text-white font-display font-extrabold text-lg shadow-lg">
            A
          </div>
          <span className="font-display font-bold text-xl tracking-tight text-theme-text">
            Ascendrite
          </span>
        </Link>

        {/* Global Controls */}
        <div className="flex items-center gap-4 relative">
          {/* Theme Dropdown Toggle */}
          <div className="relative">
            <button 
              id="btn-theme-selector"
              onClick={() => setShowThemeDropdown(!showThemeDropdown)}
              className="flex items-center gap-2 border border-theme-border text-theme-text hover:bg-theme-border px-3 py-2 rounded-lg text-sm font-semibold transition-all select-none"
            >
              <FaPalette className="text-theme-accent" />
              <span className="hidden sm:inline">Theme</span>
            </button>
            
            {showThemeDropdown && (
              <div className="absolute right-0 mt-2 w-48 bg-theme-surface border border-theme-border rounded-xl shadow-2xl py-2 z-50 animate-fade-in">
                {themes.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => changeTheme(t.id)}
                    className={`w-full text-left px-4 py-2 text-xs font-semibold hover:bg-theme-border transition-all ${
                      activeTheme === t.id ? 'text-theme-accent bg-theme-bg bg-opacity-40' : 'text-theme-text'
                    }`}
                  >
                    {t.name}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Direct Login Trigger */}
          <button 
            id="btn-header-login"
            onClick={() => setShowLoginModal(true)}
            className="bg-theme-accent hover:opacity-90 text-white text-sm font-bold px-4 py-2 rounded-lg shadow-md transition-all active:scale-95 flex items-center gap-2"
          >
            <FaGoogle size={12} />
            <span>Sign In</span>
          </button>
        </div>
      </div>

      {/* Auth Portal Overlay Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm p-4">
          <div className="bg-theme-surface border border-theme-border rounded-2xl max-w-sm w-full p-6 shadow-2xl relative">
            <h3 className="font-display font-bold text-2xl text-theme-text mb-2">Welcome to Ascendrite</h3>
            <p className="text-sm text-theme-subtle mb-6">Access course tracking, save notes bookmarks, and test your knowledge.</p>
            
            <button
              id="btn-modal-google"
              onClick={() => alert('Google Sign In callback integration triggered!')}
              className="w-full py-3 bg-theme-accent hover:opacity-90 text-white font-bold rounded-xl shadow-lg flex items-center justify-center gap-3 transition-all active:scale-95 cursor-pointer"
            >
              <FaGoogle />
              <span>Continue with Google</span>
            </button>
            
            <button
              id="btn-modal-close"
              onClick={() => setShowLoginModal(false)}
              className="w-full text-center text-xs font-semibold text-theme-subtle hover:text-theme-text mt-4 cursor-pointer"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
