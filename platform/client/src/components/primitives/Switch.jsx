import React, { useId } from 'react';

export function Switch({
  checked = false,
  onChange,
  label,
  disabled = false,
  className = '',
  ...props
}) {
  const switchId = useId();

  const handleKeyDown = (e) => {
    if (disabled) return;
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      onChange(!checked);
    }
  };

  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      <button
        id={switchId}
        type="button"
        role="switch"
        aria-checked={checked}
        aria-readonly={disabled}
        disabled={disabled}
        onKeyDown={handleKeyDown}
        onClick={() => !disabled && onChange(!checked)}
        className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
          checked ? 'bg-theme-accent' : 'bg-theme-border'
        }`}
        {...props}
      >
        <span
          aria-hidden="true"
          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
            checked ? 'translate-x-5' : 'translate-x-0'
          }`}
        />
      </button>
      
      {label && (
        <label
          htmlFor={switchId}
          onClick={() => !disabled && onChange(!checked)}
          className={`text-xs font-semibold text-theme-subtle cursor-pointer ${
            disabled ? 'cursor-not-allowed opacity-50' : ''
          }`}
        >
          {label}
        </label>
      )}
    </div>
  );
}
