import React from 'react';
import { Users, MessageSquare } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';

export default function CollaborationPage() {
  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      <div>
        <h1 className="font-display font-extrabold text-3xl text-theme-text">Collaboration Hub</h1>
        <p className="text-xs text-theme-subtle mt-1">Real-time team workspaces and shared curriculum notes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center gap-3">
            <div className="p-2 rounded-xl bg-theme-accent/10 text-theme-accent shrink-0">
              <MessageSquare className="h-5 w-5" />
            </div>
            <div>
              <CardTitle>Discussion Threads</CardTitle>
              <CardDescription>Share summaries and debate solutions.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="text-xs text-theme-subtle leading-relaxed">
            Collaborative threads are integrated directly inside lesson topic views. Navigate to any active topic in your Learning Path to read, post, or react to shared notes with peer computer scientists.
          </CardContent>
        </Card>

        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center gap-3">
            <div className="p-2 rounded-xl bg-theme-accent/10 text-theme-accent shrink-0">
              <Users className="h-5 w-5" />
            </div>
            <div>
              <CardTitle>Peer-Led Reviews</CardTitle>
              <CardDescription>Collaborate on content authoring pipelines.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="text-xs text-theme-subtle leading-relaxed">
            Ascendrite utilizes peer-review gates for all content additions. Users with Contributor roles can draft subjects inside the Creator Platform and submit them for peer-moderated governance review.
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
