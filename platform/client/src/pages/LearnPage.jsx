import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { BookOpen, Lock, Unlock, CheckCircle2, Clock, ArrowRight, Sparkles, ChevronRight, AlertTriangle } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Badge } from '../components/primitives/Badge';
import { Spinner } from '../components/primitives/Spinner';
import { useAuthStore } from '../store/authStore';
import api from '../utils/api';
import { userStorage } from '../utils/userStorage';

export default function LearnPage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const [pathway, setPathway] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const trackInterest = user?.preferences?.interest || 'web-development';

  useEffect(() => {
    let active = true;

    async function loadPathway() {
      const subjectIdMap = {
        'ai': 'machine-learning',
        'core-cs': 'os',
        'software-engineering': 'system-design',
        'web-development': 'reactjs'
      };
      const subjectId = subjectIdMap[trackInterest] || 'reactjs';
      
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Request Timeout: Server took too long to respond')), 8000)
      );

      try {
        setLoading(true);
        setError(false);
        setErrorMessage('');
        
        const res = await Promise.race([
          api.get(`/curriculum/subject/${subjectId}`),
          timeoutPromise
        ]);
        
        if (!active) return;

        // Fetch namespaced completed topics history
        const completedHistory = userStorage.getItem(user, 'ascendrite-completed-topics', []);
        
        // Enrich dynamic backend modules with local completion state namespaces
        const enrichedModules = res.data.modules.map(mod => {
          const isCompleted = mod.topics ? mod.topics.some(t => {
            const tid = t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            return completedHistory.includes(tid) || completedHistory.includes(mod.id);
          }) : completedHistory.includes(mod.id);

          return {
            ...mod,
            completed: isCompleted,
            unlocked: mod.unlocked || isCompleted
          };
        });

        setPathway({
          title: res.data.name + ' Pathway',
          description: res.data.metadata.description || 'Master structured conceptual pipelines.',
          modules: enrichedModules
        });
      } catch (err) {
        if (!active) return;
        console.error('Failed to load dynamic subject pathway:', err);
        setError(true);
        if (err.message && err.message.includes('Timeout')) {
          setErrorMessage('The connection timed out after 8 seconds. Please verify backend service responsiveness.');
        } else {
          setErrorMessage('Failed to load curriculum subjects from the database. Please verify backend database seeds are loaded.');
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    if (user) {
      loadPathway();
    }

    return () => {
      active = false;
    };
  }, [trackInterest, user, retryCount]);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-[50vh]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !pathway) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center p-8 select-none">
        <AlertTriangle className="h-12 w-12 text-theme-accent mb-4 animate-pulse-soft" />
        <h3 className="font-display font-bold text-xl text-theme-text mb-2">Subject Pathway Offline</h3>
        <p className="text-theme-subtle text-sm max-w-sm mb-6 leading-relaxed">
          {errorMessage || 'Failed to load curriculum subjects from the database. Please verify backend database seeds are loaded.'}
        </p>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setRetryCount(prev => prev + 1)}>
            Retry Connection
          </Button>
          <Button variant="subtle" onClick={() => navigate('/')}>
            Back to Home
          </Button>
        </div>
      </div>
    );
  }

  // Calculate progress details
  const totalModules = pathway.modules.length;
  const completedModules = pathway.modules.filter(m => m.completed).length;
  const progressPercent = totalModules > 0 ? Math.round((completedModules / totalModules) * 100) : 0;

  // Identify next unlocked incomplete target
  const nextTarget = pathway.modules.find(m => m.unlocked && !m.completed) || pathway.modules[0];

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      
      {/* Header section with Dynamic Progress */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-theme-border/60 pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <BookOpen className="h-6 w-6 text-theme-accent shrink-0" />
            <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-theme-text">
              {pathway.title}
            </h1>
          </div>
          <p className="text-xs text-theme-subtle max-w-xl leading-relaxed">
            {pathway.description}
          </p>
        </div>

        {/* Progress Card */}
        <div className="bg-theme-surface border border-theme-border rounded-xl p-4 w-full md:w-64 space-y-2">
          <div className="flex justify-between text-xs font-semibold">
            <span className="text-theme-subtle">Syllabus Progress</span>
            <span className="text-theme-text">{progressPercent}% Completed</span>
          </div>
          <div className="w-full h-2 bg-theme-border rounded-full overflow-hidden">
            <div 
              className="h-full bg-theme-accent transition-all duration-500" 
              style={{ width: `${progressPercent}%` }} 
            />
          </div>
          <p className="text-[10px] text-theme-subtle font-mono">
            {completedModules} of {totalModules} modules mastered
          </p>
        </div>
      </div>

      {/* Continue Learning Jump Banner */}
      {nextTarget && (
        <Card className="hover:border-theme-accent/30 transition-colors">
          <CardHeader className="flex flex-row items-center gap-3 mb-2">
            <div className="p-2 rounded-xl bg-theme-accent/10 text-theme-accent shrink-0">
              <Sparkles className="h-5 w-5 animate-pulse-soft" />
            </div>
            <div>
              <CardTitle>Continue Learning</CardTitle>
              <CardDescription>Resume your custom study pathway right where you left off.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h4 className="text-base font-bold text-theme-text">{nextTarget.title}</h4>
              <p className="text-xs text-theme-subtle mt-0.5">{nextTarget.description}</p>
            </div>
            <Button variant="primary" icon={ArrowRight} onClick={() => navigate('/workspace')}>
              Start Module
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Module Roadmap Tree Timeline */}
      <div className="flex flex-col gap-6 max-w-4xl mx-auto w-full mt-4">
        <h3 className="font-display font-extrabold text-lg text-theme-text">
          Roadmap Progression
        </h3>
        
        <div className="relative border-l border-theme-border/80 pl-6 space-y-8 ml-3">
          {pathway.modules.map((mod) => {
            const isCompleted = mod.completed;
            const isUnlocked = mod.unlocked;
            
            return (
              <div key={mod.id} className="relative group">
                
                {/* Timeline node icon switcher */}
                <div className={`absolute -left-[35px] top-1.5 w-7 h-7 rounded-full flex items-center justify-center border-2 shadow-sm transition-colors duration-300 ${
                  isCompleted 
                    ? 'bg-theme-accent border-theme-accent text-white' 
                    : isUnlocked 
                      ? 'bg-theme-surface border-theme-accent text-theme-accent'
                      : 'bg-theme-surface border-theme-border text-theme-subtle'
                }`}>
                  {isCompleted ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : isUnlocked ? (
                    <Unlock className="h-3.5 w-3.5" />
                  ) : (
                    <Lock className="h-3.5 w-3.5" />
                  )}
                </div>

                {/* Module Details Card */}
                <Card className={`transition-all duration-200 ${
                  !isUnlocked 
                    ? 'opacity-70 border-dashed bg-theme-surface/50 pointer-events-none' 
                    : 'hover:border-theme-accent/50 hover:shadow-md'
                }`}>
                  <CardHeader className="flex flex-row items-start justify-between gap-4 mb-2">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <CardTitle className="text-base font-bold">{mod.title}</CardTitle>
                        {isCompleted && (
                          <Badge variant="accent" className="py-0">Mastered</Badge>
                        )}
                        {!isUnlocked && (
                          <Badge variant="secondary" className="py-0 flex items-center gap-1">
                            <Lock className="h-2.5 w-2.5" />
                            <span>Locked</span>
                          </Badge>
                        )}
                      </div>
                      <CardDescription>{mod.description}</CardDescription>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      <div className="flex items-center gap-1 text-xs text-theme-subtle">
                        <Clock className="h-3.5 w-3.5" />
                        <span>{mod.duration}</span>
                      </div>
                      <Badge variant="primary">{mod.difficulty}</Badge>
                    </div>
                  </CardHeader>

                  {/* Progressive topics outline list slot */}
                  <CardContent className="border-t border-theme-border/50 pt-4 mt-2">
                    <span className="text-[10px] font-bold text-theme-subtle uppercase tracking-wider block mb-2">
                      Concept Nodes Included
                    </span>
                    <div className="flex flex-wrap gap-2">
                      {mod.topics.map(topic => {
                        const contentNode = (
                          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-theme-bg/60 border border-theme-border text-xs text-theme-text hover:border-theme-accent/40 transition-colors">
                            <ChevronRight className="h-3 w-3 text-theme-accent" />
                            <span>{topic}</span>
                          </div>
                        );
                        return isUnlocked ? (
                          <Link key={topic} to={`/learn/${mod.id}`}>
                            {contentNode}
                          </Link>
                        ) : (
                          <div key={topic} className="opacity-60 select-none">
                            {contentNode}
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>

                </Card>

              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
