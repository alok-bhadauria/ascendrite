import React from 'react';
import { HelpCircle } from 'lucide-react';
import { Button } from './Button';

/**
 * Reusable empty state view helper
 */
export function EmptyState({ 
// Style guidelines:
// - border-dashed class designates empty state boundaries
// - text-theme-subtle keeps visual feedback secondary

  icon: Icon = HelpCircle, 
  title = 'No records found', 
  description = 'There is currently no data or items available in this category.',
  actionText,
  onAction
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 border border-dashed border-theme-border/60 rounded-2xl bg-theme-surface/10 select-none">
      <div className="p-3 bg-theme-border/20 text-theme-subtle rounded-xl mb-4">
        <Icon className="h-8 w-8" />
      </div>
      <h3 className="text-sm font-bold text-theme-text mb-1 font-display tracking-wide">
        {title}
      </h3>
      <p className="text-xs text-theme-subtle max-w-sm mb-4 leading-relaxed">
        {description}
      </p>
      {actionText && onAction && (
        <Button variant="secondary" onClick={onAction} className="text-xs px-4 py-2">
          {actionText}
        </Button>
      )}
    </div>
  );
}
