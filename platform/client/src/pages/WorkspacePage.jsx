import React from 'react';
import { Cpu } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';

export default function WorkspacePage() {
  return (
    <div className="page-container py-12 flex-1 flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <Cpu className="h-8 w-8 text-theme-accent" />
        <h1 className="font-display font-extrabold text-3xl text-theme-text">
          Learner Workspace
        </h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Personal Practice Sandbox</CardTitle>
          <CardDescription>Assemble worksheets, organize review cards, and execute interactive code blocks.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-theme-subtle">
            Active workspaces verify execution telemetry inputs against state stores dynamically.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
