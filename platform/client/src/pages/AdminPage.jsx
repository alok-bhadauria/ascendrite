import React from 'react';
import { Shield } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';

export default function AdminPage() {
  return (
    <div className="page-container py-12 flex-1 flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <Shield className="h-8 w-8 text-theme-accent" />
        <h1 className="font-display font-extrabold text-3xl text-theme-text">
          Admin Console
        </h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>System Operating Dashboard</CardTitle>
          <CardDescription>Govern environment parameters, audit access paths, check telemetry health, and track workflow statuses.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-theme-subtle">
            Administrative lookups represent composed metrics queried from all active document database layers.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
