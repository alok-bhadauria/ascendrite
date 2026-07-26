import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Button } from './Button';

/**
 * Reusable error boundary fallback state component
 */
export function ErrorState({ 
  message = 'A connection error occurred while querying the server database.', 
  onRetry 
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 border border-rose-500/10 rounded-2xl bg-rose-950/5 select-none">
      <div className="p-3 bg-rose-500/10 text-rose-400 rounded-xl mb-4 animate-pulse-soft">
        <AlertCircle className="h-8 w-8" />
      </div>
      <h3 className="text-sm font-bold text-theme-text mb-1 font-display tracking-wide">
        Query Sync Interrupted
      </h3>
      <p className="text-xs text-theme-subtle max-w-sm mb-4 leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry} className="text-xs px-4 py-2 hover:border-rose-500/20">
          Retry Connection
        </Button>
      )}
    </div>
  );
}
