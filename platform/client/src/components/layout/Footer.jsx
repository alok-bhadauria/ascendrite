import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-theme-surface border-t border-theme-border py-8 mt-auto transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 select-none">
          <div className="w-6 h-6 rounded bg-theme-accent flex items-center justify-center text-white font-display font-extrabold text-sm shadow">
            A
          </div>
          <span className="font-display font-bold text-sm text-theme-text tracking-tight">
            Ascendrite
          </span>
        </div>
        <p className="text-xs text-theme-subtle text-center sm:text-left">
          &copy; {new Date().getFullYear()} Ascendrite. Engineered for industry-ready CS education.
        </p>
      </div>
    </footer>
  );
}
