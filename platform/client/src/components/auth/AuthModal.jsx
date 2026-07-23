import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { X, Eye, EyeOff, Loader2, ChevronLeft, ChevronRight } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../../utils/api';
import './AuthModal.css';

// ── Phase state machine ─────────────────────────────────────────────────────
// 'hidden'  → not rendered
// 'opening' → enter animation plays (next frame → 'visible')
// 'visible' → fully open
// 'closing' → exit animation plays (300ms → 'hidden')
//
// Form state is NEVER reset on close so users don't lose their input.
// It is only cleared on a successful login / register.

export function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [phase, setPhase] = useState('hidden');
  const [activeView, setActiveView] = useState('login');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const closeTimerRef = useRef(null);
  const scrollYRef = useRef(0);

  // ── Persistent form states (never reset on close) ─────────────────────
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [registerData, setRegisterData] = useState({
    firstName: '', lastName: '', email: '', password: '', confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const loginEmailRef = useRef(null);
  const registerFirstNameRef = useRef(null);
  const triggerElementRef = useRef(null);

  const navigate = useNavigate();
  const location = useLocation();

  // ── Focus shifts when modal state opens / transitions ────────────────
  useEffect(() => {
    if (phase === 'visible') {
      if (activeView === 'login') {
        loginEmailRef.current?.focus();
      } else {
        registerFirstNameRef.current?.focus();
      }
    }
  }, [phase, activeView]);

  // ── Track and restore focus on open/close lifecycle ──────────────────
  useEffect(() => {
    if (isOpen) {
      triggerElementRef.current = document.activeElement;
    } else if (phase === 'hidden' && triggerElementRef.current) {
      triggerElementRef.current.focus();
    }
  }, [isOpen, phase]);

  // ── Phase transitions ─────────────────────────────────────────────────
  useEffect(() => {
    if (isOpen) {
      clearTimeout(closeTimerRef.current);
      setPhase('opening');
      // Let the DOM paint 'opening' class first, then switch to 'visible'
      requestAnimationFrame(() => {
        requestAnimationFrame(() => setPhase('visible'));
      });
    } else {
      if (phase === 'hidden') return; // already hidden, nothing to do
      setPhase('closing');
      closeTimerRef.current = setTimeout(() => setPhase('hidden'), 320);
    }
    return () => clearTimeout(closeTimerRef.current);
  }, [isOpen]);

  // ── Body class → drives any active overlay state (no scroll locking) ───
  useEffect(() => {
    const active = phase !== 'hidden';
    document.body.classList.toggle('auth-modal-open', active);
    return () => {
      document.body.classList.remove('auth-modal-open');
    };
  }, [phase]);

  // ── ESC key ───────────────────────────────────────────────────────────
  useEffect(() => {
    if (phase === 'hidden') return;
    const handler = (e) => { if (e.key === 'Escape') handleClose(); };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [phase]);

  // ── URL sync ─────────────────────────────────────────────────────────
  useEffect(() => {
    if (isOpen && location.pathname !== '/login') {
      navigate('/login', { replace: false });
    }
  }, [isOpen]);

  // ── Don't render at all while fully hidden ────────────────────────────
  if (phase === 'hidden') return null;

  // ── Close handler ─────────────────────────────────────────────────────
  const handleClose = () => {
    setError('');
    setPhase('closing');
    closeTimerRef.current = setTimeout(() => {
      setPhase('hidden');
      onClose(); // Parent will hide state and update URL after transition is done
    }, 280);
  };

  // ── Clear forms only after successful auth ────────────────────────────
  const clearForms = () => {
    setLoginData({ email: '', password: '' });
    setRegisterData({ firstName: '', lastName: '', email: '', password: '', confirmPassword: '' });
    setShowPassword(false);
    setShowConfirm(false);
  };

  // ── Google auth callback placeholder ──────────────────────────────────
  const handleGoogleLogin = () => {
    alert("Google authentication callback triggered.");
  };

  // ── Login submit ──────────────────────────────────────────────────────
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const res = await api.post('/auth/login', loginData);
      if (onAuthSuccess) onAuthSuccess(res.data.user);
      clearForms();
      handleClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally { setLoading(false); }
  };

  // ── Register submit ───────────────────────────────────────────────────
  const { password, confirmPassword } = registerData;
  const hasLength = password.length >= 8;
  const hasNumber = /\d/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  const isPwDirty = password.length > 0;
  const isCfDirty = confirmPassword.length > 0;
  const pwMatch = password === confirmPassword && isCfDirty;

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    if (!pwMatch) { setError('Passwords do not match.'); return; }
    if (!hasLength || !hasNumber || !hasUpper || !hasSpecial) {
      setError('Password does not meet the requirements.'); return;
    }
    setLoading(true); setError('');
    try {
      await api.post('/auth/signup', {
        email: registerData.email, password,
        first_name: registerData.firstName, last_name: registerData.lastName,
      });
      const loginRes = await api.post('/auth/login', {
        email: registerData.email, password,
      });
      if (onAuthSuccess) onAuthSuccess(loginRes.data.user);
      clearForms();
      handleClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Try again.');
    } finally { setLoading(false); }
  };

  // ── Shared input class ────────────────────────────────────────────────
  const inputCls = [
    'bg-theme-bg border border-theme-border rounded-lg px-3 py-2.5 text-sm',
    'w-full focus:border-theme-accent outline-none transition-colors',
    'placeholder:text-theme-subtle text-theme-text',
  ].join(' ');

  // ── Overlay CSS class based on phase ─────────────────────────────────
  const overlayClass = [
    'auth-modal-overlay',
    phase === 'opening' ? 'auth-opening' : '',
    phase === 'visible' ? 'auth-visible' : '',
    phase === 'closing' ? 'auth-closing' : '',
  ].filter(Boolean).join(' ');

  // ── Portal to <body> to escape fixed header containment ──────────────
  return createPortal(
    <div
      className={overlayClass}
      onClick={handleClose}
      role="dialog"
      aria-modal="true"
      aria-label="Authentication"
    >
      <div
        className="auth-card bg-theme-surface border border-theme-border"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          className="auth-close-btn text-theme-subtle hover:text-theme-accent hover:bg-theme-border"
          onClick={handleClose}
          aria-label="Close"
        >
          <X size={18} />
        </button>

        {/* Sliding gradient panel */}
        <div className={`card-bg ${activeView === 'login' ? 'login' : ''}`} />

        {/* Hero: visible when Register form is active (left side) */}
        <div className={`hero register ${activeView === 'register' ? 'active' : ''}`}>
          <div className="hero-logo">A</div>
          <h2 className="font-display font-bold text-2xl leading-tight">Already Registered?</h2>
          <p className="text-sm opacity-85 leading-relaxed">
            Login to access your personalised dashboard<br />and continue learning.
          </p>
          <button type="button" onClick={() => setActiveView('login')} className="hero-toggle-btn flex items-center justify-center gap-1">
            <ChevronLeft size={18} className="shrink-0" />
            <span>Login Here</span>
          </button>
        </div>

        {/* Register form (right side when active) */}
        <div className={`form register text-theme-text ${activeView === 'register' ? 'active' : ''}`}>
          <h2 className="font-display font-bold text-2xl text-theme-accent mb-1">Sign Up</h2>
          <p className="text-xs text-theme-subtle mb-3">Join Ascendrite and start learning</p>

          <button type="button" className="google-btn text-theme-text hover:bg-theme-border transition-all w-full flex items-center justify-center gap-2 mb-2" onClick={handleGoogleLogin}>
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" width="16" height="16" />
            <span>Continue with Google</span>
          </button>

          <div className="flex items-center gap-2 w-full mb-3 opacity-60">
            <div className="h-[1px] bg-theme-border flex-1"></div>
            <span className="text-[10px] text-theme-subtle font-bold uppercase tracking-wider">or sign up with email</span>
            <div className="h-[1px] bg-theme-border flex-1"></div>
          </div>

          {error && (
            <p className="text-xs text-red-500 font-semibold bg-red-500/10 border border-red-500/20 px-3 py-2 rounded-lg w-full mb-2">
              {error}
            </p>
          )}

          <form onSubmit={handleRegisterSubmit} className="w-full flex flex-col gap-2.5">
            <div className="flex gap-2">
              <input ref={registerFirstNameRef} className={inputCls} type="text" placeholder="First name" required
                value={registerData.firstName}
                onChange={(e) => setRegisterData({ ...registerData, firstName: e.target.value })} />
              <input className={inputCls} type="text" placeholder="Last name" required
                value={registerData.lastName}
                onChange={(e) => setRegisterData({ ...registerData, lastName: e.target.value })} />
            </div>
            <input className={inputCls} type="email" placeholder="Email address" required
              value={registerData.email}
              onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })} />
            <div className="relative w-full">
              <input className={inputCls} type={showPassword ? 'text' : 'password'} placeholder="Password" required
                value={registerData.password}
                onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })} />
              <button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-theme-subtle hover:text-theme-accent"
                onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
              </button>
            </div>
            <div className="relative w-full">
              <input className={inputCls} type={showConfirm ? 'text' : 'password'} placeholder="Confirm password" required
                value={registerData.confirmPassword}
                onChange={(e) => setRegisterData({ ...registerData, confirmPassword: e.target.value })} />
              <button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-theme-subtle hover:text-theme-accent"
                onClick={() => setShowConfirm(!showConfirm)}>
                {showConfirm ? <EyeOff size={15} /> : <Eye size={15} />}
              </button>
            </div>

            {isCfDirty ? (
              <div className="password-feedback-container">
                {pwMatch
                  ? <span className="text-green-500 font-semibold text-xs">✓ Passwords match</span>
                  : <span className="text-red-500  font-semibold text-xs">✗ Passwords do not match</span>}
              </div>
            ) : isPwDirty ? (
              <div className="password-feedback-container">
                <span className="text-theme-subtle font-semibold text-[10px] mb-0.5">Requirements</span>
                <div className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-[10px] font-semibold">
                  <span className={hasLength ? 'text-green-500' : 'text-red-500'}>{hasLength ? '✓' : '✗'} 8+ characters</span>
                  <span className={hasNumber ? 'text-green-500' : 'text-red-500'}>{hasNumber ? '✓' : '✗'} Number</span>
                  <span className={hasUpper ? 'text-green-500' : 'text-red-500'}>{hasUpper ? '✓' : '✗'} Uppercase</span>
                  <span className={hasSpecial ? 'text-green-500' : 'text-red-500'}>{hasSpecial ? '✓' : '✗'} Special char</span>
                </div>
              </div>
            ) : null}

            <button type="submit" disabled={loading}
              className="w-full bg-theme-accent hover:opacity-90 hover:scale-[1.015] hover:shadow-lg hover:shadow-theme-accent/20 text-white font-bold py-2.5 rounded-lg text-sm flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-[0.98] mt-1 disabled:opacity-60">
              {loading && <Loader2 className="animate-spin" size={15} />}
              SIGN UP
            </button>
          </form>
        </div>

        {/* Hero: visible when Login form is active (right side) */}
        <div className={`hero login ${activeView === 'login' ? 'active' : ''}`}>
          <div className="hero-logo">A</div>
          <h2 className="font-display font-bold text-2xl leading-tight">Welcome to<br />Ascendrite</h2>
          <p className="text-sm opacity-85 leading-relaxed">
            Create an account to track your progress<br />and customise your learning journey.
          </p>
          <button type="button" onClick={() => setActiveView('register')} className="hero-toggle-btn flex items-center justify-center gap-1">
            <span>New User ? Register Here</span>
            <ChevronRight size={18} className="shrink-0" />
          </button>
        </div>

        {/* Login form (left side when active) */}
        <div className={`form login text-theme-text ${activeView === 'login' ? 'active' : ''}`}>
          <h2 className="font-display font-bold text-2xl text-theme-accent mb-1">Login</h2>
          <p className="text-xs text-theme-subtle mb-3">Welcome back to Ascendrite</p>

          <button type="button" className="google-btn text-theme-text hover:bg-theme-border transition-all w-full flex items-center justify-center gap-2 mb-2" onClick={handleGoogleLogin}>
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" width="16" height="16" />
            <span>Continue with Google</span>
          </button>

          <div className="flex items-center gap-2 w-full mb-3 opacity-60">
            <div className="h-[1px] bg-theme-border flex-1"></div>
            <span className="text-[10px] text-theme-subtle font-bold uppercase tracking-wider">or login with email</span>
            <div className="h-[1px] bg-theme-border flex-1"></div>
          </div>

          {error && (
            <p className="text-xs text-red-500 font-semibold bg-red-500/10 border border-red-500/20 px-3 py-2 rounded-lg w-full mb-2">
              {error}
            </p>
          )}

          <form onSubmit={handleLoginSubmit} className="w-full flex flex-col gap-3">
            <input ref={loginEmailRef} className={inputCls} type="email" placeholder="Email address" required
              value={loginData.email}
              onChange={(e) => setLoginData({ ...loginData, email: e.target.value })} />
            <div className="relative w-full">
              <input className={inputCls} type={showPassword ? 'text' : 'password'} placeholder="Password" required
                value={loginData.password}
                onChange={(e) => setLoginData({ ...loginData, password: e.target.value })} />
              <button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-theme-subtle hover:text-theme-accent"
                onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
              </button>
            </div>
            <a href="#" className="text-xs text-theme-subtle hover:text-theme-accent self-end transition-colors"
              onClick={(e) => e.preventDefault()}>
              Forgot password?
            </a>
            <button type="submit" disabled={loading}
              className="w-full bg-theme-accent hover:opacity-90 hover:scale-[1.015] hover:shadow-lg hover:shadow-theme-accent/20 text-white font-bold py-2.5 rounded-lg text-sm flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-[0.98] disabled:opacity-60">
              {loading && <Loader2 className="animate-spin" size={15} />}
              LOGIN
            </button>
          </form>
        </div>

        {/* Mobile: switch link */}
        <div className="auth-mobile-switch">
          {activeView === 'login' ? (
            <p className="text-xs text-theme-subtle flex flex-col items-center gap-2">
              <span>No account?</span>
              <button className="mobile-toggle-btn" onClick={() => setActiveView('register')}>
                <span>Sign Up Here</span>
                <ChevronRight size={14} className="shrink-0 text-theme-accent" />
              </button>
            </p>
          ) : (
            <p className="text-xs text-theme-subtle flex flex-col items-center gap-2">
              <span>Have an account?</span>
              <button className="mobile-toggle-btn" onClick={() => setActiveView('login')}>
                <ChevronLeft size={14} className="shrink-0 text-theme-accent" />
                <span>Login</span>
              </button>
            </p>
          )}
        </div>
      </div>
    </div>,
    document.body   // ← portal: renders outside <header>, at body level
  );
}

export default AuthModal;
