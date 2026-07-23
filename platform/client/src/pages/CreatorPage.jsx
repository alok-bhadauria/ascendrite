import React from 'react';
import { PenTool } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';

export default function CreatorPage() {
  return (
    <div className="page-container py-12 flex-1 flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <PenTool className="h-8 w-8 text-theme-accent" />
        <h1 className="font-display font-extrabold text-3xl text-theme-text">
          Creator Workspace
        </h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Content Authoring Console</CardTitle>
          <CardDescription>Draft dynamic subjects, curriculum nodes, assessment questions, and validation schema criteria.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-theme-subtle">
            Publishing workflows pass validation pipelines before resource insertion is executed on backend storage.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
