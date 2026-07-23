import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, ListTodo, FileText, Activity, Sparkles, Plus, Trash2, CheckCircle2 } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Input } from '../components/primitives/Input';
import { TextArea } from '../components/primitives/TextArea';
import { useAuthStore } from '../store/authStore';

export default function WorkspacePage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  // ── Study Planner / Tasks State ──────────────────────────────────────────
  const [tasks, setTasks] = useState(() => {
    const saved = localStorage.getItem('ascendrite-workspace-tasks');
    return saved ? JSON.parse(saved) : [
      { id: 1, text: 'Review linear regression mathematical derivation rules', completed: false },
      { id: 2, text: 'Test interactive sorting simulator with custom arrays', completed: true },
      { id: 3, text: 'Analyze database query indexes and execution plan schemas', completed: false }
    ];
  });

  const [newTaskText, setNewTaskText] = useState('');

  // ── Personal Notes State ────────────────────────────────────────────────
  const [notes, setNotes] = useState(() => {
    return localStorage.getItem('ascendrite-workspace-notes') || 
      "## Study Notes\nJot down thoughts, derivations, or loop state mappings here. This workspace is persisted automatically.";
  });

  // Sync state helpers
  useEffect(() => {
    localStorage.setItem('ascendrite-workspace-tasks', JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    localStorage.setItem('ascendrite-workspace-notes', notes);
  }, [notes]);

  const addTask = (e) => {
    e.preventDefault();
    if (!newTaskText.trim()) return;
    const newTask = {
      id: Date.now(),
      text: newTaskText.trim(),
      completed: false
    };
    setTasks([...tasks, newTask]);
    setNewTaskText('');
  };

  const toggleTask = (id) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(t => t.id !== id));
  };

  // Determine track preferences dynamically
  const trackInterest = user?.preferences?.interest || 'web-development';
  const trackGoal = user?.preferences?.objective || 'Strengthen fundamentals';

  const tracksMap = {
    'ai': { name: 'Artificial Intelligence', nextTopic: 'Deep Learning Feed-Forward Networks' },
    'core-cs': { name: 'Core Computer Science', nextTopic: 'Operating Systems & Thread Locks' },
    'software-engineering': { name: 'Software Engineering', nextTopic: 'Object-Oriented System Design' },
    'web-development': { name: 'Web Development', nextTopic: 'Full-Stack Express & SQL Integrations' }
  };

  const activeTrack = tracksMap[trackInterest] || tracksMap['web-development'];

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      
      {/* ── Header Welcome Row ────────────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-theme-border/60 pb-6">
        <div>
          <h1 className="font-display font-extrabold text-3xl text-theme-text">
            My Workspace
          </h1>
          <p className="text-xs text-theme-subtle mt-1">
            Track: <span className="font-semibold text-theme-text">{activeTrack.name}</span> | Objective: <span className="font-semibold text-theme-text">{trackGoal}</span>
          </p>
        </div>
        <Button variant="primary" icon={BookOpen} onClick={() => navigate('/learn')}>
          Continue Journey
        </Button>
      </div>

      {/* ── Core Workspace Grid ────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side (8 cols): Goals, Planner, Notes */}
        <div className="lg:col-span-8 flex flex-col gap-8 w-full">
          
          {/* Active Study Path */}
          <Card className="hover:border-theme-accent/30 transition-colors">
            <CardHeader className="flex flex-row items-center gap-3 mb-2">
              <div className="p-2 rounded-xl bg-theme-accent/10 text-theme-accent shrink-0">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Recommended Next Step</CardTitle>
                <CardDescription>Based on your primary interest selection guidelines.</CardDescription>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-theme-bg border border-theme-border rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <span className="text-[10px] font-mono text-theme-accent uppercase font-bold tracking-wider">Active Node</span>
                  <h4 className="text-base font-bold text-theme-text mt-1">{activeTrack.nextTopic}</h4>
                  <p className="text-xs text-theme-subtle mt-0.5">Estimated Duration: 45 minutes | Concept Complexity: High</p>
                </div>
                <Button variant="secondary" onClick={() => navigate('/learn')}>
                  Begin Section
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Notion-inspired Study notes block */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 mb-2">
              <div className="p-2 rounded-xl bg-theme-border/30 text-theme-text shrink-0">
                <FileText className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Scratchpad & Code Notes</CardTitle>
                <CardDescription>Write markdown explanations, loop parameters, or derivations.</CardDescription>
              </div>
            </CardHeader>
            <CardContent>
              <TextArea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={8}
                className="font-mono text-xs leading-relaxed"
                placeholder="Markdown text..."
              />
            </CardContent>
          </Card>
        </div>

        {/* Right Side (4 cols): Study Planner, Milestones */}
        <div className="lg:col-span-4 flex flex-col gap-8 w-full">
          
          {/* Planner Tasks Card */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 mb-2">
              <div className="p-2 rounded-xl bg-theme-border/30 text-theme-text shrink-0">
                <ListTodo className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Study Planner</CardTitle>
                <CardDescription>Track target topics and assessments.</CardDescription>
              </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              {/* Task list container */}
              <div className="flex flex-col gap-2">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-start justify-between gap-2 bg-theme-bg/60 border border-theme-border rounded-xl p-3">
                    <button
                      onClick={() => toggleTask(task.id)}
                      className={`flex items-start gap-2.5 cursor-pointer text-left focus:outline-none ${
                        task.completed ? 'text-theme-subtle line-through' : 'text-theme-text'
                      }`}
                    >
                      <CheckCircle2 className={`h-4.5 w-4.5 shrink-0 mt-0.5 ${task.completed ? 'text-theme-accent' : 'text-theme-border'}`} />
                      <span className="text-xs leading-normal">{task.text}</span>
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="text-theme-subtle hover:text-theme-accent shrink-0 cursor-pointer p-0.5 focus:outline-none"
                      aria-label="Delete task"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))}
              </div>

              {/* Add task form */}
              <form onSubmit={addTask} className="flex gap-2 border-t border-theme-border pt-4">
                <Input
                  value={newTaskText}
                  onChange={(e) => setNewTaskText(e.target.value)}
                  placeholder="New target task..."
                  className="py-2 text-xs"
                />
                <Button type="submit" variant="secondary" className="px-3 py-2 shrink-0">
                  <Plus className="h-4 w-4" />
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Activity Milestone timeline */}
          <Card>
            <CardHeader className="flex flex-row items-center gap-3 mb-2">
              <div className="p-2 rounded-xl bg-theme-border/30 text-theme-text shrink-0">
                <Activity className="h-5 w-5" />
              </div>
              <div>
                <CardTitle>Recent Milestones</CardTitle>
                <CardDescription>Activity logs tracked by the Learning engine.</CardDescription>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4 relative pl-4 border-l border-theme-border">
                <div className="relative">
                  <div className="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-theme-accent border-2 border-theme-surface" />
                  <span className="text-[10px] font-mono text-theme-subtle">Today</span>
                  <h5 className="text-xs font-bold text-theme-text mt-0.5">Enriched learning direction setup</h5>
                  <p className="text-[10.5px] text-theme-subtle mt-0.5">Onboarding objectives parsed successfully.</p>
                </div>
                <div className="relative">
                  <div className="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-theme-border border-2 border-theme-surface" />
                  <span className="text-[10px] font-mono text-theme-subtle">Yesterday</span>
                  <h5 className="text-xs font-bold text-theme-text mt-0.5">Authorized ecosystem access</h5>
                  <p className="text-[10.5px] text-theme-subtle mt-0.5">Local session validation rules compiled.</p>
                </div>
              </div>
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
