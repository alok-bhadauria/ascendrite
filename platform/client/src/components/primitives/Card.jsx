import React from 'react';

export function Card({
  children,
  className = '',
  ...props
}) {
  return (
    <div
      className={`bg-theme-surface border border-theme-border rounded-2xl p-6 transition-all duration-200 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '', ...props }) {
  return (
    <div className={`flex flex-col gap-1 mb-4 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className = '', ...props }) {
  return (
    <h3 className={`font-display font-bold text-lg text-theme-text ${className}`} {...props}>
      {children}
    </h3>
  );
}

export function CardDescription({ children, className = '', ...props }) {
  return (
    <p className={`text-xs text-theme-subtle leading-relaxed ${className}`} {...props}>
      {children}
    </p>
  );
}

export function CardContent({ children, className = '', ...props }) {
  return (
    <div className={`text-sm text-theme-text/90 ${className}`} {...props}>
      {children}
    </div>
  );
}
