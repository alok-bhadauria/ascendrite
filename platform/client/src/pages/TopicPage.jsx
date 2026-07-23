import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { ChevronLeft, BookOpen, Download, Bookmark, FileText, CheckCircle2, ArrowRight, AlertTriangle, MessageSquare, Send, Sparkles } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Badge } from '../components/primitives/Badge';
import { Input } from '../components/primitives/Input';
import { TextArea } from '../components/primitives/TextArea';
import { Spinner } from '../components/primitives/Spinner';

// Dynamic mock topics content mapped by ID
const topicsContent = {
  'ml-foundations': {
    title: 'Linear Regressions & Gradient Fit',
    duration: '45m',
    difficulty: 'Medium',
    content: `Linear regression maps a scalar response to one or more explanatory variables using linear predictor functions. The weights are updated iteratively using the **Gradient Descent** optimization algorithm:

$$ \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta) $$

Where $J(\theta)$ represents the Mean Squared Error (MSE) cost function:

$$ J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2 $$

By minimizing this loss matrix, the model aligns the regression predictor line to the training coordinate parameters.`,
    attachments: [
      { name: 'regression_gradient_descent_proof.pdf', size: '1.4 MB' },
      { name: 'mse_loss_matrix_derivation.pdf', size: '890 KB' }
    ],
    nextId: 'deep-learning',
    nextTitle: 'Deep Learning Networks'
  },
  'deep-learning': {
    title: 'Backpropagation Calculus & Network Layers',
    duration: '60m',
    difficulty: 'Hard',
    content: `Backpropagation calculates the gradient of the error function with respect to the neural network's weights. It applies the multi-variable **Chain Rule** calculus layer by layer:

$$ \frac{\partial E}{\partial w_{ij}} = \frac{\partial E}{\partial a_{j}} \cdot \frac{\partial a_j}{\partial w_{ij}} $$

By propagating error derivatives backward from the output layer, weights are fine-tuned to match expected values.`,
    attachments: [
      { name: 'backprop_chain_rule_calculus.pdf', size: '2.1 MB' },
      { name: 'neural_weights_matrix_ref.xlsx', size: '420 KB' }
    ],
    nextId: 'multi-agents',
    nextTitle: 'Multi-Agent Architectures'
  }
};

export default function TopicPage() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  // ── Universal State Simulators (Loading / Errors) ──────────────────────
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [localNotes, setLocalNotes] = useState('');
  const [completed, setCompleted] = useState(false);
  
  // Comments and discussion board state
  const [comments, setComments] = useState([]);
  const [newCommentText, setNewCommentText] = useState('');

  const topicData = topicsContent[topicId] || topicsContent['ml-foundations'];

  // Sync state on load
  useEffect(() => {
    // Hydrate bookmarks
    const savedBookmarks = JSON.parse(localStorage.getItem('ascendrite-bookmarks') || '[]');
    setIsBookmarked(savedBookmarks.includes(topicId));

    // Hydrate local notes
    const savedNotes = localStorage.getItem(`ascendrite-notes-${topicId}`) || '';
    setLocalNotes(savedNotes);

    // Hydrate comments
    const savedComments = JSON.parse(localStorage.getItem(`ascendrite-comments-${topicId}`) || '[]');
    if (savedComments.length > 0) {
      setComments(savedComments);
    } else {
      setComments([
        { id: 'c-1', author: 'Alok Bhadauria', text: 'The mathematical step for Mean Squared Error minimization outlines regression weights clearly.', timestamp: '2h ago' }
      ]);
    }

    // Reset status
    setCompleted(false);
    setError(false);
  }, [topicId]);

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (!newCommentText.trim()) return;

    const newComment = {
      id: `c-${Date.now()}`,
      author: 'Author Account',
      text: newCommentText.trim(),
      timestamp: 'Just now'
    };

    const updatedComments = [...comments, newComment];
    setComments(updatedComments);
    localStorage.setItem(`ascendrite-comments-${topicId}`, JSON.stringify(updatedComments));
    setNewCommentText('');
  };

  const toggleBookmark = () => {
    const savedBookmarks = JSON.parse(localStorage.getItem('ascendrite-bookmarks') || '[]');
    let updated;
    if (isBookmarked) {
      updated = savedBookmarks.filter(id => id !== topicId);
    } else {
      updated = [...savedBookmarks, topicId];
    }
    localStorage.setItem('ascendrite-bookmarks', JSON.stringify(updated));
    setIsBookmarked(!isBookmarked);
  };

  const handleNotesChange = (val) => {
    setLocalNotes(val);
    localStorage.setItem(`ascendrite-notes-${topicId}`, val);
  };

  const handleMarkMastered = () => {
    setCompleted(true);
    // Mark as completed in learning history
    const completedHistory = JSON.parse(localStorage.getItem('ascendrite-completed-topics') || '[]');
    if (!completedHistory.includes(topicId)) {
      localStorage.setItem('ascendrite-completed-topics', JSON.stringify([...completedHistory, topicId]));
    }
  };

  // Simulate loading trigger
  const triggerLoading = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1200);
  };

  // Simulate error trigger
  const triggerError = () => {
    setError(true);
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Spinner size="lg" />
        <p className="text-xs text-theme-subtle font-semibold">Fetching conceptual formulas and proofs...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8 select-none">
        <AlertTriangle className="h-12 w-12 text-theme-accent mb-4 animate-pulse-soft" />
        <h3 className="font-display font-bold text-xl text-theme-text mb-2">Service Temporarily Unavailable</h3>
        <p className="text-theme-subtle text-sm max-w-sm mb-6 leading-relaxed">
          Failed to fetch syllabus topic data from the Knowledge Platform engine.
        </p>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setError(false)}>
            Retry Connection
          </Button>
          <Button variant="subtle" onClick={() => navigate('/learn')}>
            Return to Index
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-6 select-none">
      
      {/* Navigation Breadcrumb */}
      <div className="flex items-center justify-between border-b border-theme-border/60 pb-4">
        <Link to="/learn" className="flex items-center gap-1.5 text-xs font-semibold text-theme-subtle hover:text-theme-text transition-colors">
          <ChevronLeft className="h-4 w-4" />
          <span>Back to Pathway</span>
        </Link>

        {/* Diagnostic Simulator triggers */}
        <div className="flex gap-2">
          <button 
            onClick={triggerLoading}
            className="text-[10px] font-bold text-theme-subtle hover:text-theme-text border border-theme-border px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
          >
            Mock Load State
          </button>
          <button 
            onClick={triggerError}
            className="text-[10px] font-bold text-theme-subtle hover:text-theme-text border border-theme-border px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
          >
            Mock Error Fallback
          </button>
        </div>
      </div>

      {/* Title Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2.5">
            <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-theme-text leading-tight">
              {topicData.title}
            </h1>
            <Badge variant="primary">{topicData.difficulty}</Badge>
          </div>
          <div className="flex items-center gap-3 text-xs text-theme-subtle">
            <span className="flex items-center gap-1">
              <BookOpen className="h-3.5 w-3.5" />
              <span>Read Duration: {topicData.duration}</span>
            </span>
          </div>
        </div>

        {/* Bookmark control */}
        <Button 
          variant={isBookmarked ? 'primary' : 'secondary'} 
          icon={Bookmark} 
          onClick={toggleBookmark}
        >
          {isBookmarked ? 'Bookmarked' : 'Bookmark'}
        </Button>
      </div>

      {/* Main Learning Content Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side: Text book content, math derivations */}
        <div className="lg:col-span-8 flex flex-col gap-6 w-full">
          <Card>
            <CardContent className="prose max-w-none text-theme-text/90 leading-relaxed space-y-4">
              <p className="whitespace-pre-line text-sm sm:text-base">
                {topicData.content}
              </p>
            </CardContent>
          </Card>

          {/* Practice section anchor */}
          <Card className="border-dashed hover:border-theme-accent/40 transition-colors">
            <CardHeader className="mb-2">
              <CardTitle className="text-base font-bold flex items-center gap-2">
                <Sparkles className="h-4.5 w-4.5 text-theme-accent animate-pulse-soft" />
                <span>Simulations &amp; Code Sandbox</span>
              </CardTitle>
              <CardDescription>Test regression parameters or backpropagation chain rules using interactive widgets.</CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary" onClick={() => navigate('/workspace')}>
                Open Practice Sandbox
              </Button>
            </CardContent>
          </Card>

          {/* Discussion board */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-base font-bold flex items-center gap-2">
                <MessageSquare className="h-4.5 w-4.5 text-theme-accent" />
                <span>Discussion Thread</span>
              </CardTitle>
              <CardDescription>Collaborative notes and topic explanations shared by contributors.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Existing comments */}
              <div className="flex flex-col gap-3">
                {comments.map(c => (
                  <div key={c.id} className="bg-theme-bg/50 border border-theme-border rounded-xl p-3 space-y-1">
                    <div className="flex justify-between items-center text-[10px] font-mono text-theme-subtle">
                      <span className="font-bold text-theme-text">{c.author}</span>
                      <span>{c.timestamp}</span>
                    </div>
                    <p className="text-xs text-theme-text/90 leading-relaxed">{c.text}</p>
                  </div>
                ))}
              </div>

              {/* Submit form */}
              <form onSubmit={handleCommentSubmit} className="flex gap-2 border-t border-theme-border pt-4">
                <Input
                  value={newCommentText}
                  onChange={(e) => setNewCommentText(e.target.value)}
                  placeholder="Share a conceptual note..."
                  className="py-2 text-xs"
                />
                <Button type="submit" variant="secondary" className="px-3 py-2 shrink-0">
                  <Send className="h-4 w-4" />
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {/* Right Side: Attachments, Local Notes, Completion Recommendations */}
        <div className="lg:col-span-4 flex flex-col gap-6 w-full">
          
          {/* Attachments Card */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Resource Attachments</CardTitle>
              <CardDescription>Supplementary proofs and calculations.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              {topicData.attachments.map(file => (
                <div key={file.name} className="flex items-center justify-between gap-3 bg-theme-bg/60 border border-theme-border rounded-xl p-3">
                  <div className="flex items-center gap-2.5 min-w-0">
                    <FileText className="h-4 w-4 text-theme-accent shrink-0" />
                    <span className="text-xs text-theme-text font-medium truncate">{file.name}</span>
                  </div>
                  <button className="text-theme-subtle hover:text-theme-accent p-1 cursor-pointer transition-colors focus:outline-none" aria-label="Download attachment">
                    <Download className="h-3.5 w-3.5" />
                  </button>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Local notes specific to this topic */}
          <Card>
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Topic Notes</CardTitle>
              <CardDescription>Saved automatically to this section.</CardDescription>
            </CardHeader>
            <CardContent>
              <TextArea
                value={localNotes}
                onChange={(e) => handleNotesChange(e.target.value)}
                placeholder="Ex. Remember chain rule multiplications step..."
                rows={5}
                className="text-xs leading-normal"
              />
            </CardContent>
          </Card>

          {/* Mastered & Continue recommendations panel */}
          <Card className="bg-theme-accent/5 border-theme-accent/25">
            <CardHeader className="mb-2">
              <CardTitle className="text-sm font-bold">Progress Flow</CardTitle>
              <CardDescription>Confirm mastery to unlock the next conceptual module.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {!completed ? (
                <Button variant="primary" className="w-full" icon={CheckCircle2} onClick={handleMarkMastered}>
                  Mark as Mastered
                </Button>
              ) : (
                <div className="space-y-3 animate-fade-in">
                  <div className="flex items-center gap-2 text-green-500 font-bold text-xs">
                    <CheckCircle2 className="h-4 w-4 shrink-0" />
                    <span>Mastery Registered successfully!</span>
                  </div>
                  {topicData.nextId && (
                    <div className="border-t border-theme-border/50 pt-3 space-y-2">
                      <span className="text-[10px] font-bold text-theme-subtle uppercase tracking-wider block">Recommended Next</span>
                      <Link 
                        to={`/learn/${topicData.nextId}`}
                        className="flex items-center justify-between p-3 rounded-xl bg-theme-bg border border-theme-border hover:border-theme-accent/40 text-xs font-semibold text-theme-text transition-all group"
                      >
                        <span className="truncate">{topicData.nextTitle}</span>
                        <ArrowRight className="h-3.5 w-3.5 text-theme-accent group-hover:translate-x-1 transition-transform shrink-0" />
                      </Link>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
