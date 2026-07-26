import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';

/**
 * Reusable modal container primitive with standard visual identity
 * Complies with WAI-ARIA and controls focus management.
 */
export function Modal({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) {
  const overlayRef = useRef(null);
  const previousFocusRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement;
      
      const handleKeyDown = (e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };
      
      window.addEventListener('keydown', handleKeyDown);
      // Disable background scrolling when open
      document.body.style.overflow = 'hidden';
      
      return () => {
        window.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = '';
        if (previousFocusRef.current) {
          previousFocusRef.current.focus();
        }
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div 
      ref={overlayRef}
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in pointer-events-auto"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div 
        className={`w-full ${maxWidth} bg-theme-surface border border-theme-border rounded-2xl shadow-elevated overflow-hidden flex flex-col`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header section */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-theme-border/60">
          <h3 id="modal-title" className="text-sm font-bold font-display text-theme-text tracking-wide">
            {title}
          </h3>
          <button
            onClick={onClose}
            className="text-theme-subtle hover:text-theme-text transition-colors p-1 rounded cursor-pointer shrink-0 focus:outline-none focus:ring-2 focus:ring-theme-accent"
            aria-label="Close dialog"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Content body */}
        <div className="p-6 overflow-y-auto max-h-[80vh]">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
