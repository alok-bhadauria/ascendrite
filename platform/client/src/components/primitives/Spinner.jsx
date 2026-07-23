import React from 'react';

export function Spinner({
  size = 'md', // sm | md | lg
  className = '',
  ...props
}) {
  const sizes = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-3",
    lg: "h-12 w-12 border-4"
  };

  return (
    <div
      role="status"
      aria-label="Loading"
      className={`animate-spin rounded-full border-theme-border border-t-theme-accent ${sizes[size]} ${className}`}
      {...props}
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}
