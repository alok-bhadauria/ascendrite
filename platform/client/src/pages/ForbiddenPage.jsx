import React from 'react';
import { ShieldAlert } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { useNavigate } from 'react-router-dom';

export default function ForbiddenPage() {
  const navigate = useNavigate();

  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center p-8 select-none">
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-64 h-64 bg-theme-accent opacity-5 rounded-full blur-3xl pointer-events-none" />
      <ShieldAlert className="h-16 w-16 text-theme-accent mb-6 animate-pulse-soft" />
      <h1 className="font-display font-extrabold text-3xl text-theme-text mb-4">
        Access Denied
      </h1>
      <p className="text-theme-subtle text-sm max-w-md mb-8 leading-relaxed">
        Your current actor security profile is missing the required platform capabilities to access this experience channel.
      </p>
      <Button variant="secondary" onClick={() => navigate('/')}>
        Return to Portal
      </Button>
    </div>
  );
}
