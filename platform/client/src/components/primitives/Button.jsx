import React from 'react';

export function Button({
  children,
  variant = 'primary', // primary | secondary | subtle
  size = 'md',        // sm | md | lg
  loading = false,
  disabled = false,
  className = '',
  icon: Icon,
  ...props
}) {
  const baseStyle = "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent focus-visible:ring-offset-2 cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 select-none active:scale-[0.98]";
  
  const variants = {
    primary: "bg-theme-accent text-white hover:opacity-90 shadow-sm",
    secondary: "bg-theme-surface text-theme-text border border-theme-border hover:bg-theme-border/50",
    subtle: "bg-transparent text-theme-subtle hover:text-theme-text hover:bg-theme-surface/40"
  };

  const sizes = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-5 py-2.5 text-sm",
    lg: "px-7 py-3 text-base"
  };

  return (
    <button
      disabled={disabled || loading}
      aria-busy={loading}
      className={`${baseStyle} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {loading ? (
        <span className="mr-2 animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full" aria-hidden="true" />
      ) : Icon ? (
        <span className="mr-2" aria-hidden="true"><Icon className="h-4 w-4" /></span>
      ) : null}
      {children}
    </button>
  );
}
