import React from 'react';
import { BookOpen } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';

export default function LearnPage() {
  return (
    <div className="page-container py-12 flex-1 flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <BookOpen className="h-8 w-8 text-theme-accent" />
        <h1 className="font-display font-extrabold text-3xl text-theme-text">
          Learning Paths
        </h1>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Master Computer Science</CardTitle>
          <CardDescription>Select a dynamic topic subject tracker below to explore LaTeX algorithm weight derivations and interactive trace execution blocks.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-theme-subtle">
            Curriculum content streams are queried directly from the Knowledge Platform repository boundaries.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
