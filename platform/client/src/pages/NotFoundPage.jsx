import React from 'react';
import { HelpCircle } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { useNavigate } from 'react-router-dom';

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center p-8 select-none">
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-64 h-64 bg-theme-accent opacity-5 rounded-full blur-3xl pointer-events-none" />
      <HelpCircle className="h-16 w-16 text-theme-subtle mb-6" />
      <h1 className="font-display font-extrabold text-3xl text-theme-text mb-4">
        Page Not Found
      </h1>
      <p className="text-theme-subtle text-sm max-w-md mb-8 leading-relaxed">
        The requested path does not exist inside the Ascendrite ecosystem navigation map.
      </p>
      <Button variant="secondary" onClick={() => navigate('/')}>
        Return to Portal
      </Button>
    </div>
  );
}
