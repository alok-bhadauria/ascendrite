import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { ChevronLeft, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Input } from '../components/primitives/Input';
import { TextArea } from '../components/primitives/TextArea';
import { Switch } from '../components/primitives/Switch';
import { Badge } from '../components/primitives/Badge';

export default function AuthoringPage() {
  const { draftId } = useParams();
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('ai');
  const [content, setContent] = useState('');
  const [status, setStatus] = useState('draft');
  const [isPreview, setIsPreview] = useState(false);
  const [saving, setSaving] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [validationErrors, setValidationErrors] = useState([]);

  // ── Load draft from localStorage ─────────────────────────────────────────
  useEffect(() => {
    const savedDrafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
    const draft = savedDrafts.find(d => d.id === draftId);
    if (draft) {
      setTitle(draft.title);
      setCategory(draft.category);
      setContent(draft.content || '');
      setStatus(draft.status || 'draft');
    } else {
      // Setup mock defaults
      setTitle('New Curriculum Topic');
      setCategory('ai');
      setContent('');
      setStatus('draft');
    }
  }, [draftId]);

  // ── Auto-save simulation ──────────────────────────────────────────────────
  useEffect(() => {
    if (!title) return; // avoid saving default empty render
    const delayDebounceFn = setTimeout(() => {
      setSaving(true);
      const savedDrafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
      const index = savedDrafts.findIndex(d => d.id === draftId);
      
      const updatedDraft = {
        id: draftId,
        title,
        category,
        content,
        status,
        lastModified: 'Just now'
      };

      if (index > -1) {
        savedDrafts[index] = updatedDraft;
      } else {
        savedDrafts.unshift(updatedDraft);
      }

      localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(savedDrafts));
      setTimeout(() => setSaving(false), 600);
    }, 1500);

    return () => clearTimeout(delayDebounceFn);
  }, [title, category, content, status]);

  // ── Run validation routines ──────────────────────────────────────────────
  const runValidations = () => {
    const errors = [];
    if (!title.trim() || title === 'New Curriculum Topic' || title === 'Untitled Subject Draft') {
      errors.push('Title must be a descriptive curriculum name.');
    }
    if (content.length < 20) {
      errors.push('Content body must contain at least 20 characters of instruction.');
    }
    setValidationErrors(errors);
    return errors.length === 0;
  };

  const handlePublishSubmit = () => {
    const isValid = runValidations();
    if (!isValid) return;

    setPublishing(true);
    setTimeout(() => {
      setStatus('published');
      // Update local storage status
      const savedDrafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
      const index = savedDrafts.findIndex(d => d.id === draftId);
      if (index > -1) {
        savedDrafts[index].status = 'published';
        localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(savedDrafts));
      }
      setPublishing(false);
      navigate('/creator');
    }, 1200);
  };

  const handleSubmitForReview = () => {
    const isValid = runValidations();
    if (!isValid) return;

    setStatus('ready_for_review');
    const savedDrafts = JSON.parse(localStorage.getItem('ascendrite-creator-drafts') || '[]');
    const index = savedDrafts.findIndex(d => d.id === draftId);
    if (index > -1) {
      savedDrafts[index].status = 'ready_for_review';
      localStorage.setItem('ascendrite-creator-drafts', JSON.stringify(savedDrafts));
    }
  };

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-6 select-none">
      
      {/* Breadcrumb row */}
      <div className="flex items-center justify-between border-b border-theme-border/60 pb-4">
        <Link to="/creator" className="flex items-center gap-1.5 text-xs font-semibold text-theme-subtle hover:text-theme-text transition-colors">
          <ChevronLeft className="h-4 w-4" />
          <span>Back to Workspace</span>
        </Link>

        {/* Auto save indicator */}
        <div className="flex items-center gap-2 text-xs text-theme-subtle">
          {saving ? (
            <>
              <Loader2 className="h-3.5 w-3.5 animate-spin text-theme-accent" />
              <span>Saving changes...</span>
            </>
          ) : (
            <>
              <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
              <span>All changes saved to drafts cache</span>
            </>
          )}
        </div>
      </div>

      {/* Editor Header controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="font-display font-extrabold text-2xl text-theme-text leading-tight">
            Authoring Workspace
          </h2>
          <p className="text-xs text-theme-subtle mt-0.5">Draft ID: {draftId} | Status: <span className="font-bold text-theme-text uppercase">{status}</span></p>
        </div>

        {/* Preview toggle switch */}
        <div className="flex items-center gap-3">
          <Switch 
            checked={isPreview} 
            onChange={setIsPreview} 
            label="Preview Content Mode" 
          />
        </div>
      </div>

      {/* Main Authoring Form Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Columns (8 cols): Input Forms / Preview Container */}
        <div className="lg:col-span-8 flex flex-col gap-6 w-full">
          {isPreview ? (
            <Card className="min-h-[300px]">
              <CardHeader className="mb-2">
                <div className="flex items-center gap-2.5">
                  <CardTitle className="text-xl font-bold">{title}</CardTitle>
                  <Badge variant="primary">{category.toUpperCase()}</Badge>
                </div>
                <CardDescription>Rendered output visualization</CardDescription>
              </CardHeader>
              <CardContent className="prose max-w-none text-theme-text/90 leading-relaxed mt-4 whitespace-pre-line border-t border-theme-border/50 pt-4">
                {content || <span className="text-theme-subtle italic">No content written yet. Toggle preview off to write content.</span>}
              </CardContent>
            </Card>
          ) : (
            <Card className="space-y-5">
              <Input
                label="Topic Subject Name"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Ex. Attention Matrix Calculus"
                required
              />

              <div className="flex flex-col gap-1.5 w-full">
                <label className="text-xs font-semibold text-theme-subtle">
                  Curriculum Track Category
                </label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="bg-theme-surface text-theme-text border border-theme-border rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-theme-accent transition-colors duration-200"
                >
                  <option value="ai">Artificial Intelligence</option>
                  <option value="core-cs">Core Computer Science</option>
                  <option value="software-engineering">Software Engineering</option>
                  <option value="web-development">Web Development</option>
                </select>
              </div>

              <TextArea
                label="Syllabus Content Body (Markdown / LaTeX)"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write your equations and syllabus contents here..."
                rows={10}
                required
              />
            </Card>
          )}
        </div>

        {/* Right Columns (4 cols): Moderation Actions & Val Errors */}
        <div className="lg:col-span-4 flex flex-col gap-6 w-full">
          
          {/* Moderation Workflow Controller */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Publishing Pipeline</CardTitle>
              <CardDescription>Submit modifications for review or update published catalog records.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              {status !== 'published' ? (
                <>
                  <Button 
                    variant="secondary" 
                    className="w-full"
                    onClick={handleSubmitForReview}
                    disabled={status === 'ready_for_review'}
                  >
                    {status === 'ready_for_review' ? 'In Review Queue' : 'Submit for Review'}
                  </Button>
                  <Button 
                    variant="primary" 
                    className="w-full" 
                    onClick={handlePublishSubmit}
                    loading={publishing}
                  >
                    Publish Draft
                  </Button>
                </>
              ) : (
                <div className="text-center py-2">
                  <CheckCircle2 className="h-10 w-10 text-green-500 mx-auto mb-2" />
                  <p className="text-xs font-semibold text-theme-text">Topic is Published</p>
                  <p className="text-[10px] text-theme-subtle mt-0.5">This subject is locked inside the production syllabus database.</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Validation Checklist Panel */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Validation Status</CardTitle>
              <CardDescription>Mandatory checks required for publishing.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Errors check list */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 text-xs font-semibold">
                  <span className={title.trim().length > 3 && title !== 'Untitled Subject Draft' ? 'text-green-500' : 'text-red-500'}>
                    {title.trim().length > 3 && title !== 'Untitled Subject Draft' ? '✓' : '✗'}
                  </span>
                  <span className="text-theme-text">Descriptive Topic Title</span>
                </div>
                <div className="flex items-center gap-2 text-xs font-semibold">
                  <span className={content.length >= 20 ? 'text-green-500' : 'text-red-500'}>
                    {content.length >= 20 ? '✓' : '✗'}
                  </span>
                  <span className="text-theme-text">Minimum Content Body length</span>
                </div>
              </div>

              {validationErrors.length > 0 && (
                <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-3 flex gap-2 animate-fade-in">
                  <AlertTriangle className="h-4.5 w-4.5 text-red-500 shrink-0 mt-0.5" />
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] font-bold text-red-500 uppercase tracking-wider">Publishing Blocked</span>
                    {validationErrors.map((err, idx) => (
                      <p key={idx} className="text-[11px] text-theme-text leading-tight">{err}</p>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
