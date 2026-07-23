import React from 'react';

export function Badge({
  children,
  variant = 'primary', // primary | secondary | accent
  className = '',
  ...props
}) {
  const baseStyle = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold select-none border";
  
  const variants = {
    primary: "bg-theme-surface text-theme-text border-theme-border",
    secondary: "bg-theme-border/20 text-theme-subtle border-transparent",
    accent: "bg-theme-accent/10 text-theme-accent border-theme-accent/20"
  };

  return (
    <span
      className={`${baseStyle} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}
