import React, { useId } from 'react';

export function Input({
  label,
  description,
  error,
  type = 'text',
  className = '',
  disabled = false,
  required = false,
  ...props
}) {
  const inputId = useId();
  const descId = useId();
  const errorId = useId();

  return (
    <div className="flex flex-col gap-1.5 w-full">
      {label && (
        <label htmlFor={inputId} className="text-xs font-semibold text-theme-subtle">
          {label}
          {required && <span className="text-theme-accent ml-1" aria-hidden="true">*</span>}
        </label>
      )}
      
      <input
        id={inputId}
        type={type}
        disabled={disabled}
        required={required}
        aria-invalid={!!error}
        aria-describedby={`${description ? descId : ''} ${error ? errorId : ''}`.trim() || undefined}
        className={`w-full bg-theme-surface text-theme-text border border-theme-border rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-theme-accent transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed ${error ? 'border-theme-accent' : ''} ${className}`}
        {...props}
      />

      {description && !error && (
        <p id={descId} className="text-xs text-theme-subtle/80">
          {description}
        </p>
      )}

      {error && (
        <p id={errorId} className="text-xs text-theme-accent font-medium animate-fade-in" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
