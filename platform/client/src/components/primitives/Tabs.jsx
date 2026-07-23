import React, { createContext, useContext } from 'react';

const TabsContext = createContext(null);

export function Tabs({
  value,
  onValueChange,
  children,
  className = '',
  ...props
}) {
  return (
    <TabsContext.Provider value={{ value, onValueChange }}>
      <div className={`w-full ${className}`} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

export function TabsList({
  children,
  className = '',
  ariaLabel = 'Tab Options',
  ...props
}) {
  return (
    <div
      role="tablist"
      aria-label={ariaLabel}
      className={`inline-flex items-center gap-1 bg-theme-surface border border-theme-border p-1 rounded-xl ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function TabsTrigger({
  value,
  children,
  className = '',
  disabled = false,
  ...props
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsTrigger must be used inside a Tabs component');

  const isActive = context.value === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      disabled={disabled}
      onClick={() => !disabled && context.onValueChange(value)}
      className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent select-none cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 ${
        isActive
          ? 'bg-theme-bg text-theme-text shadow-sm'
          : 'text-theme-subtle hover:text-theme-text'
      } ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export function TabsContent({
  value,
  children,
  className = '',
  ...props
}) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsContent must be used inside a Tabs component');

  const isActive = context.value === value;

  if (!isActive) return null;

  return (
    <div
      role="tabpanel"
      tabIndex={0}
      className={`mt-4 outline-none focus-visible:ring-2 focus-visible:ring-theme-accent focus-visible:ring-offset-2 rounded-xl ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
