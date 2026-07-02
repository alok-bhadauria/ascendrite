import React, { useState, useEffect, useRef } from 'react';
import { Palette, ChevronDown, LogIn, LogOut, Star } from 'lucide-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthModal } from '../auth/AuthModal';

const themes = [
  { id: 'carbon', name: 'Carbon', preview: { bg: '#151515', surface: '#1d1d1d', text: '#f6f6f6', accent: '#f44336' } },
  { id: 'nord-light', name: 'Nord Light', preview: { bg: '#eceff4', surface: '#d8dee9', text: '#2e3440', accent: '#5e81ac' } },
  { id: 'dracula', name: 'Dracula', preview: { bg: '#282a36', surface: '#343746', text: '#f8f8f2', accent: '#bd93f9' } },
  { id: 'sepia', name: 'Sepia', preview: { bg: '#f4edd8', surface: '#ebe3cc', text: '#5b4636', accent: '#8d6e63' } },
  { id: 'matrix', name: 'Matrix', preview: { bg: '#050805', surface: '#0b0f0b', text: '#b3ffb3', accent: '#00ff00' } },
  { id: 'milkshake', name: 'Milkshake', preview: { bg: '#ffffff', surface: '#f5f5f5', text: '#222222', accent: '#e91e63' } }
];

export default function Navbar() {
  const [activeTheme, setActiveTheme]       = useState('nord-light');
  const [showThemeDropdown, setShowThemeDropdown] = useState(false);
  const [showAuthModal, setShowAuthModal]   = useState(false);
  const [currentUser, setCurrentUser]       = useState(null);

  const navigate         = useNavigate();
  const location         = useLocation();
  const themeSelectorRef = useRef(null);

  // Auto-open modal when navigating directly to /login
  useEffect(() => {
    if (location.pathname === '/login' && !showAuthModal) {
      setShowAuthModal(true);
    }
    if (location.pathname !== '/login' && showAuthModal) {
      setShowAuthModal(false);
    }
  }, [location.pathname]);

  useEffect(() => {
    if (!showThemeDropdown) return;

    const handleOutsideClick = (e) => {
      if (themeSelectorRef.current && !themeSelectorRef.current.contains(e.target)) {
        setShowThemeDropdown(false);
      }
    };

    const handleScroll = () => {
      setShowThemeDropdown(false);
    };

    document.addEventListener('mousedown', handleOutsideClick);
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
      window.removeEventListener('scroll', handleScroll);
    };
  }, [showThemeDropdown]);

  useEffect(() => {
    const savedTheme = localStorage.getItem('ascendrite-theme') || 'nord-light';
    setActiveTheme(savedTheme);
    
    // Check if token exists in cookie or localStorage to auto login
    const savedUser = localStorage.getItem('ascendrite-user');
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }
  }, []);

  const changeTheme = (themeId) => {
    localStorage.setItem('ascendrite-theme', themeId);
    document.documentElement.setAttribute('data-theme', themeId);
    setActiveTheme(themeId);
    setShowThemeDropdown(false);
  };

  const handleAuthSuccess = (user) => {
    setCurrentUser(user);
    localStorage.setItem('ascendrite-user', JSON.stringify(user));
  };

  const handleLogoClick = (e) => {
    if (window.location.pathname === '/') {
      e.preventDefault();
      const startPosition = window.pageYOffset || document.documentElement.scrollTop;
      const distance = -startPosition;
      const easeInOutCubic = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const duration = 1000;
      let startTime = null;

      const animation = (currentTime) => {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progressRatio = easeInOutCubic(Math.min(timeElapsed / duration, 1));
        window.scrollTo(0, startPosition + distance * progressRatio);
        if (timeElapsed < duration) {
          requestAnimationFrame(animation);
        }
      };
      requestAnimationFrame(animation);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('ascendrite-user');
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-theme-bg bg-opacity-70 backdrop-blur-md border-b border-theme-border transition-all duration-200 w-full max-w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" onClick={handleLogoClick} className="flex items-center gap-2 select-none group">
          <div className="w-8 h-8 rounded-lg bg-theme-accent text-white flex items-center justify-center font-display font-extrabold text-lg shadow-md group-hover:scale-105 transition-transform">
            A
          </div>
          <span className="font-display font-bold text-xl tracking-tight text-theme-text">
            Ascendrite
          </span>
        </Link>


        {/* Global Controls */}
        <div className="flex items-center gap-4 relative">
          
          {/* Theme Selector Dropdown (with Color Dots Previews) */}
          <div className="relative" ref={themeSelectorRef}>
            <button 
              id="btn-theme-selector"
              onClick={() => setShowThemeDropdown(!showThemeDropdown)}
              className="flex items-center gap-2 border border-theme-border text-theme-text hover:bg-theme-border px-3 py-2 rounded-lg text-sm font-semibold transition-all select-none cursor-pointer"
            >
              <Palette className="text-theme-accent" size={16} />
              <span className="hidden sm:inline font-bold">Theme</span>
              <ChevronDown size={14} className="opacity-60" />
            </button>
            
            <div className={`absolute -right-20 sm:right-0 mt-2 w-80 bg-theme-surface border border-theme-border rounded-xl shadow-2xl p-3 z-50 flex flex-col gap-2 transition-all duration-300 origin-top-right transform ${
              showThemeDropdown 
                ? 'opacity-100 scale-100 translate-y-0 pointer-events-auto' 
                : 'opacity-0 scale-95 -translate-y-2 pointer-events-none'
            }`}>
              <span className="font-mono text-[10px] text-theme-subtle uppercase tracking-wider font-bold px-1 select-none">
                Select theme
              </span>
              <div className="grid grid-cols-2 gap-2">
                {themes.map((t) => {
                  const isSelected = activeTheme === t.id;
                  return (
                    <button
                      key={t.id}
                      onClick={() => changeTheme(t.id)}
                      style={{
                        backgroundColor: t.preview.surface,
                        color: t.preview.text,
                        borderColor: isSelected ? t.preview.accent : 'transparent'
                      }}
                      className={`px-2.5 py-2 text-[10.5px] font-mono font-bold rounded-lg transition-all hover:scale-[1.03] flex items-center justify-between gap-1.5 cursor-pointer select-none shadow-sm border-2`}
                    >
                      <div className="flex items-center gap-1 min-w-0">
                        {isSelected ? (
                          <Star size={9} className="shrink-0 fill-current text-theme-accent" />
                        ) : (
                          <div className="w-[9px] h-[9px] shrink-0" />
                        )}
                        <span className="truncate leading-none">{t.name}</span>
                      </div>
                      <div className="flex items-center gap-1 shrink-0">
                        <span className="w-2.5 h-2.5 rounded-full border border-neutral-400/10" style={{ backgroundColor: t.preview.bg }} />
                        <span className="w-2.5 h-2.5 rounded-full border border-neutral-400/10" style={{ backgroundColor: t.preview.text }} />
                        <span className="w-2.5 h-2.5 rounded-full border border-neutral-400/10" style={{ backgroundColor: t.preview.accent }} />
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* User Section / Login Portal Triggers */}
          {!currentUser ? (
            <button 
              id="btn-header-login"
              onClick={() => {
                setShowAuthModal(true);
                if (location.pathname !== '/login') {
                  navigate('/login', { preventScrollReset: true });
                }
              }}
              className="bg-theme-accent hover:opacity-90 hover:scale-[1.03] hover:shadow-lg hover:shadow-theme-accent/15 text-white text-sm font-bold px-4 py-2 rounded-lg transition-all active:scale-[0.97] duration-200 flex items-center gap-2 cursor-pointer"
            >
              <LogIn size={15} />
              <span>Login</span>
            </button>
          ) : (
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex flex-col text-right">
                <span className="text-xs font-bold text-theme-text leading-tight">{currentUser.first_name} {currentUser.last_name}</span>
                <span className="text-[10px] text-theme-subtle">{currentUser.email}</span>
              </div>
              
              <button 
                id="btn-header-logout"
                onClick={handleLogout}
                className="border border-theme-border text-theme-text hover:bg-theme-accent hover:text-white px-3 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-1.5 cursor-pointer"
              >
                <LogOut size={14} />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Sliding Authentication Modal Overlay */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => {
          setShowAuthModal(false);
          // If URL is /login, return to home keeping scroll exactly as it is
          if (location.pathname === '/login') {
            navigate('/', { replace: true, preventScrollReset: true });
          }
        }}
        onAuthSuccess={handleAuthSuccess}
      />
    </header>
  );
}
