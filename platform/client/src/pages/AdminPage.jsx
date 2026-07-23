import React, { useState, useEffect } from 'react';
import { Shield, Users, PenTool, CheckCircle2, Activity } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Switch } from '../components/primitives/Switch';

export default function AdminPage() {
  // ── platform configuration states ───────────────────────────────────────
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [debugLogs, setDebugLogs] = useState(true);

  // ── platform data counts ────────────────────────────────────────────────
  const [completedCount, setCompletedCount] = useState(0);
  const [reviewQueue, setReviewQueue] = useState([]);

  useEffect(() => {
    // Read completed count
    const completed = JSON.parse(localStorage.getItem('ascendrite-completed-topics') || '[]');
    setCompletedCount(completed.length);

    // Read creator drafts in review queue
    const drafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
    const inReview = drafts.filter(d => d.status === 'ready_for_review');
    setReviewQueue(inReview);
  }, []);

  const handleApproveDraft = (id) => {
    const drafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
    const index = drafts.findIndex(d => d.id === id);
    if (index > -1) {
      drafts[index].status = 'published';
      localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(drafts));
    }
    // Update local queue state
    setReviewQueue(reviewQueue.filter(d => d.id !== id));
  };

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-theme-border/60 pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-theme-accent shrink-0" />
            <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-theme-text">
              Admin OS Portal
            </h1>
          </div>
          <p className="text-xs text-theme-subtle">
            Ecosystem governance dashboard. Monitor server health, approve drafts, and manage global settings.
          </p>
        </div>
      </div>

      {/* Numerical Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-5xl">
        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between pb-2 mb-0">
            <CardTitle className="text-xs font-bold text-theme-subtle uppercase tracking-wider">Mastered Topics</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-theme-accent" />
          </CardHeader>
          <CardContent className="mt-1">
            <h3 className="font-display font-extrabold text-4xl text-theme-text">{completedCount}</h3>
            <p className="text-[10px] text-theme-subtle mt-1"> মাস্টারড topics completed across tracks</p>
          </CardContent>
        </Card>

        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between pb-2 mb-0">
            <CardTitle className="text-xs font-bold text-theme-subtle uppercase tracking-wider">Pending Review</CardTitle>
            <PenTool className="h-4 w-4 text-theme-accent" />
          </CardHeader>
          <CardContent className="mt-1">
            <h3 className="font-display font-extrabold text-4xl text-theme-text">{reviewQueue.length}</h3>
            <p className="text-[10px] text-theme-subtle mt-1">Creator drafts in moderation queue</p>
          </CardContent>
        </Card>

        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between pb-2 mb-0">
            <CardTitle className="text-xs font-bold text-theme-subtle uppercase tracking-wider">Active Sessions</CardTitle>
            <Users className="h-4 w-4 text-theme-accent" />
          </CardHeader>
          <CardContent className="mt-1">
            <h3 className="font-display font-extrabold text-4xl text-theme-text">14</h3>
            <p className="text-[10px] text-theme-subtle mt-1">User actors validated in last 5m</p>
          </CardContent>
        </Card>
      </div>

      {/* Content Moderation & platform settings section grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side (8 cols): Content Moderation Queue */}
        <div className="lg:col-span-8 flex flex-col gap-6 w-full">
          <h3 className="font-display font-extrabold text-lg text-theme-text">
            Syllabus Moderation Queue
          </h3>

          {reviewQueue.length === 0 ? (
            <Card className="border-dashed py-12 text-center">
              <CheckCircle2 className="h-10 w-10 text-green-500 mx-auto mb-4 animate-pulse-soft" />
              <CardTitle className="text-base font-bold">Queue Clean</CardTitle>
              <CardDescription>No pending creator drafts waiting for moderation approvals.</CardDescription>
            </Card>
          ) : (
            <div className="flex flex-col gap-3">
              {reviewQueue.map(draft => (
                <div key={draft.id} className="bg-theme-surface border border-theme-border rounded-2xl p-5 flex items-center justify-between gap-4">
                  <div className="space-y-1 min-w-0">
                    <h4 className="text-sm font-bold text-theme-text truncate">{draft.title}</h4>
                    <p className="text-xs text-theme-subtle truncate">{draft.content || 'No preview available'}</p>
                    <span className="text-[9px] font-mono text-theme-accent font-bold uppercase block pt-0.5">{draft.category}</span>
                  </div>
                  
                  <Button variant="primary" className="py-2 text-xs shrink-0" onClick={() => handleApproveDraft(draft.id)}>
                    Approve &amp; Publish
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Side (4 cols): Configuration controls & logs */}
        <div className="lg:col-span-4 flex flex-col gap-8 w-full">
          
          {/* Settings Control Panel */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Ecosystem Rules</CardTitle>
              <CardDescription>Toggle global platform settings.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <Switch
                checked={maintenanceMode}
                onChange={setMaintenanceMode}
                label="Maintenance Lockout"
              />
              <Switch
                checked={debugLogs}
                onChange={setDebugLogs}
                label="Forward Telemetry Logs"
              />
            </CardContent>
          </Card>

          {/* Telemetry Log Panel */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 mb-2">
              <Activity className="h-4.5 w-4.5 text-theme-accent" />
              <div>
                <CardTitle className="text-sm font-bold">Audit Telemetry</CardTitle>
                <CardDescription>Real-time ecosystem logs.</CardDescription>
              </div>
            </CardHeader>
            <CardContent className="bg-theme-bg/60 border border-theme-border rounded-xl p-3 font-mono text-[9px] text-theme-subtle leading-relaxed overflow-x-hidden">
              <p className="text-theme-text font-bold">--- Systemd logs context ---</p>
              <p className="text-green-500 mt-1">INFO: Token principal verified (Student)</p>
              <p>INFO: API endpoint GET /curriculum/subjects matched</p>
              <p>INFO: MongoDB query resolved in 14ms</p>
              {maintenanceMode && (
                <p className="text-theme-accent font-bold mt-1">WARN: Maintenance Mode Activated</p>
              )}
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
