/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useState, useCallback } from 'react';
import { X, CheckCircle2, AlertTriangle, AlertCircle, Info } from 'lucide-react';

const ToastContext = createContext(null);

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const showToast = useCallback((type, title, message, duration = 5000) => {
    const id = Date.now() + Math.random().toString(36).substr(2, 9);
    setToasts((prev) => [...prev, { id, type, title, message, duration }]);
    
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  }, [removeToast]);

  const toastIcons = {
    success: <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />,
    error: <AlertCircle className="h-5 w-5 text-rose-400 shrink-0" />,
    warning: <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0" />,
    info: <Info className="h-5 w-5 text-blue-400 shrink-0" />
  };

  const toastStyles = {
    success: 'border-emerald-500/20 bg-emerald-950/30 text-emerald-200 shadow-emerald-950/20',
    error: 'border-rose-500/20 bg-rose-950/30 text-rose-200 shadow-rose-950/20',
    warning: 'border-amber-500/20 bg-amber-950/30 text-amber-200 shadow-amber-950/20',
    info: 'border-blue-500/20 bg-blue-950/30 text-blue-200 shadow-blue-950/20'
  };

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}
      {/* Toast portal container */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none select-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto flex items-start gap-3 p-4 rounded-xl border shadow-elevated transition-all duration-200 animate-slide-in ${toastStyles[t.type] || toastStyles.info}`}
            role="alert"
          >
            {toastIcons[t.type]}
            <div className="flex-1 flex flex-col gap-0.5">
              {t.title && <h4 className="text-xs font-bold font-display tracking-wide">{t.title}</h4>}
              {t.message && <p className="text-[11px] leading-relaxed opacity-90">{t.message}</p>}
            </div>
            <button
              onClick={() => removeToast(t.id)}
              className="text-theme-subtle hover:text-theme-text transition-colors p-0.5 rounded cursor-pointer shrink-0 focus:outline-none"
              aria-label="Dismiss notification"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
