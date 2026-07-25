import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { PenTool, Plus, Edit3, Trash2, CheckCircle2, Clock, AlertCircle } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Badge } from '../components/primitives/Badge';
import { Spinner } from '../components/primitives/Spinner';
import api from '../utils/api';

export default function CreatorPage() {
  const navigate = useNavigate();

  const [drafts, setDrafts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadDrafts = async () => {
    try {
      setLoading(true);
      const res = await api.get('/creator/drafts');
      const mapped = res.data.map(d => ({
        id: d.id,
        title: d.content?.title || d.content?.name || 'Untitled Draft',
        category: d.content?.category || 'ai',
        status: d.validation_status?.toLowerCase() || 'draft',
        lastModified: d.updated_at ? new Date(d.updated_at).toLocaleDateString() : 'Just now',
        content: d.content?.body || ''
      }));
      setDrafts(mapped);
    } catch (err) {
      console.error('Failed to load drafts from server:', err);
      // fallback
      const saved = localStorage.getItem('ascendrite-creator-drafts');
      setDrafts(saved ? JSON.parse(saved) : []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDrafts();
  }, []);

  const handleCreateDraft = async () => {
    try {
      const res = await api.post('/creator/drafts', {
        resource_type: 'topic',
        content: {
          title: 'Untitled Subject Draft',
          category: 'ai',
          subject_id: 'machine-learning',
          body: ''
        }
      });
      navigate(`/creator/edit/${res.data.id}`);
    } catch (err) {
      console.error('Failed to create backend draft:', err);
      const newDraft = {
        id: `draft-${Date.now()}`,
        title: 'Untitled Subject Draft',
        category: 'ai',
        status: 'draft',
        lastModified: 'Just now',
        content: ''
      };
      const updated = [newDraft, ...drafts];
      setDrafts(updated);
      localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(updated));
      navigate(`/creator/edit/${newDraft.id}`);
    }
  };

  const handleDeleteDraft = async (id, e) => {
    e.stopPropagation();
    try {
      await api.delete(`/creator/drafts/${id}`);
      setDrafts(drafts.filter(d => d.id !== id));
    } catch (err) {
      console.error('Failed to delete backend draft:', err);
      const updated = drafts.filter(d => d.id !== id);
      setDrafts(updated);
      localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(updated));
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      draft: <Badge variant="primary">Draft</Badge>,
      ready_for_review: <Badge variant="secondary">In Review</Badge>,
      published: <Badge variant="accent">Published</Badge>
    };
    return badges[status] || badges.draft;
  };

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-theme-border/60 pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <PenTool className="h-6 w-6 text-theme-accent shrink-0" />
            <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-theme-text">
              Creator Platform
            </h1>
          </div>
          <p className="text-xs text-theme-subtle">
            Author and publish structured syllabus tracks, equations, and interactive simulations.
          </p>
        </div>
        
        <Button variant="primary" icon={Plus} onClick={handleCreateDraft}>
          Create Subject Draft
        </Button>
      </div>

      {/* Core Creator Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side (8 cols): Drafts List */}
        <div className="lg:col-span-8 flex flex-col gap-6 w-full">
          <h3 className="font-display font-extrabold text-lg text-theme-text">
            Active Draft Workspaces
          </h3>

          {loading ? (
            <div className="py-16 text-center">
              <Spinner size="lg" />
              <p className="text-xs text-theme-subtle mt-2 font-semibold">Loading drafts...</p>
            </div>
          ) : drafts.length === 0 ? (
            <Card className="border-dashed py-16 text-center">
              <AlertCircle className="h-10 w-10 text-theme-subtle mx-auto mb-4" />
              <CardTitle className="text-base font-bold">No Drafts Found</CardTitle>
              <CardDescription className="mb-6">Create a new subject draft to begin publishing content.</CardDescription>
              <Button variant="secondary" onClick={handleCreateDraft}>
                New Draft
              </Button>
            </Card>
          ) : (
            <div className="flex flex-col gap-3">
              {drafts.map((d) => (
                <div
                  key={d.id}
                  onClick={() => navigate(`/creator/edit/${d.id}`)}
                  className="bg-theme-surface border border-theme-border hover:border-theme-accent/40 rounded-2xl p-5 shadow-sm transition-all duration-200 cursor-pointer flex items-center justify-between gap-4 group"
                >
                  <div className="space-y-1 min-w-0">
                    <div className="flex items-center gap-2.5">
                      <h4 className="text-base font-bold text-theme-text truncate group-hover:text-theme-accent transition-colors">
                        {d.title}
                      </h4>
                      {getStatusBadge(d.status)}
                    </div>
                    <p className="text-xs text-theme-subtle leading-normal truncate">
                      {d.content || 'Empty draft workspace content...'}
                    </p>
                    <div className="flex items-center gap-3 text-[10px] text-theme-subtle font-mono pt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        <span>Edited: {d.lastModified}</span>
                      </span>
                      <span>•</span>
                      <span className="uppercase">{d.category}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      onClick={(e) => { e.stopPropagation(); navigate(`/creator/edit/${d.id}`); }}
                      className="p-2 rounded-lg border border-theme-border hover:bg-theme-border/40 text-theme-text cursor-pointer transition-colors focus:outline-none"
                      aria-label="Edit draft"
                    >
                      <Edit3 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={(e) => handleDeleteDraft(d.id, e)}
                      className="p-2 rounded-lg border border-theme-border hover:bg-red-500/10 hover:border-red-500/30 text-theme-subtle hover:text-red-500 cursor-pointer transition-colors focus:outline-none"
                      aria-label="Delete draft"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Side (4 cols): Quick publishing metrics queue info */}
        <div className="lg:col-span-4 flex flex-col gap-8 w-full">
          
          {/* Quick Actions Panel */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Authoring Tools</CardTitle>
              <CardDescription>Guidelines for publishing curriculum subjects.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3.5 text-xs text-theme-text/80 leading-relaxed">
              <div className="flex gap-2">
                <CheckCircle2 className="h-4 w-4 text-theme-accent shrink-0 mt-0.5" />
                <p>Include fully formatted LaTeX formula matrices for algorithm weights.</p>
              </div>
              <div className="flex gap-2">
                <CheckCircle2 className="h-4 w-4 text-theme-accent shrink-0 mt-0.5" />
                <p>Verify simulation schema mappings before submitting for moderation.</p>
              </div>
            </CardContent>
          </Card>

          {/* Recently Published items tracker */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Published Outputs</CardTitle>
              <CardDescription>Master database additions.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-3 relative pl-4 border-l border-theme-border">
                <div>
                  <span className="text-[10px] font-mono text-theme-accent font-bold block">1 day ago</span>
                  <h5 className="text-xs font-bold text-theme-text mt-0.5">Linear Regressions Cost Calculations</h5>
                  <p className="text-[10.5px] text-theme-subtle mt-0.5">Added to AI curriculum map.</p>
                </div>
                <div>
                  <span className="text-[10px] font-mono text-theme-subtle font-bold block">3 days ago</span>
                  <h5 className="text-xs font-bold text-theme-text mt-0.5">Bubble Sort Code Tracing simulation</h5>
                  <p className="text-[10.5px] text-theme-subtle mt-0.5">Unlocked globally.</p>
                </div>
              </div>
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
