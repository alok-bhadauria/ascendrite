import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, Database, Cpu, Globe, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { useAuthStore } from '../store/authStore';

const interests = [
  { id: 'ai', name: 'Artificial Intelligence', icon: Brain, desc: 'ML models and multi-agent systems' },
  { id: 'core-cs', name: 'Core Computer Science', icon: Database, desc: 'DBMS engines, threads, networks' },
  { id: 'software-engineering', name: 'Software Engineering', icon: Cpu, desc: 'System design and algorithm weights' },
  { id: 'web-development', name: 'Web Development', icon: Globe, desc: 'Full-stack client and server frameworks' }
];

const objectives = [
  'Prepare for placements',
  'Strengthen fundamentals',
  'Master a subject',
  'Build projects',
  'Explore new topics'
];

export default function OnboardingPage() {
  const { user, login } = useAuthStore();
  const [selectedInterest, setSelectedInterest] = useState('');
  const [selectedObjective, setSelectedObjective] = useState('');
  const navigate = useNavigate();

  const handleComplete = () => {
    // Enrich local principal metadata progressively
    if (user) {
      const enrichedUser = {
        ...user,
        onboarded: true,
        preferences: {
          interest: selectedInterest || 'explore',
          objective: selectedObjective || 'explore'
        }
      };
      login(enrichedUser);
    }
    navigate('/learn');
  };

  return (
    <div className="flex-1 flex items-center justify-center p-6 select-none relative min-h-[calc(100vh-140px)]">
      {/* Background radial highlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-theme-accent opacity-5 rounded-full blur-3xl pointer-events-none" />

      <Card className="max-w-xl w-full border border-theme-border shadow-2xl relative z-10">
        <CardHeader className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-theme-accent/10 text-theme-accent flex items-center justify-center mx-auto mb-4 animate-float">
            <Sparkles className="h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-extrabold font-display">
            Welcome to Ascendrite, {user?.first_name || 'Learner'}
          </CardTitle>
          <CardDescription className="text-sm">
            Let's establish your initial learning direction. You can update these anytime inside your workspace.
          </CardDescription>
        </CardHeader>

        <CardContent className="flex flex-col gap-6">
          {/* Interest Selection Section */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold text-theme-subtle uppercase tracking-wider">
              1. What is your primary learning interest?
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {interests.map((interest) => {
                const isSelected = selectedInterest === interest.id;
                return (
                  <button
                    key={interest.id}
                    onClick={() => setSelectedInterest(interest.id)}
                    className={`flex items-start gap-3 p-4 rounded-xl border text-left cursor-pointer transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent ${
                      isSelected
                        ? 'bg-theme-accent/10 border-theme-accent text-theme-text shadow-sm'
                        : 'bg-theme-surface border-theme-border text-theme-subtle hover:text-theme-text hover:border-theme-subtle/40'
                    }`}
                  >
                    <interest.icon className={`h-5 w-5 shrink-0 mt-0.5 ${isSelected ? 'text-theme-accent' : ''}`} />
                    <div className="flex flex-col">
                      <span className="text-sm font-semibold leading-tight">{interest.name}</span>
                      <span className="text-[11px] opacity-80 leading-normal mt-0.5">{interest.desc}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Objective Selection Section */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-bold text-theme-subtle uppercase tracking-wider">
              2. What is your current learning objective?
            </h4>
            <div className="flex flex-wrap gap-2">
              {objectives.map((objective) => {
                const isSelected = selectedObjective === objective;
                return (
                  <button
                    key={objective}
                    onClick={() => setSelectedObjective(objective)}
                    className={`px-4 py-2 rounded-xl border text-xs font-semibold cursor-pointer transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent ${
                      isSelected
                        ? 'bg-theme-accent/10 border-theme-accent text-theme-text'
                        : 'bg-theme-surface border-theme-border text-theme-subtle hover:text-theme-text hover:border-theme-subtle/40'
                    }`}
                  >
                    {objective}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Core Action triggers */}
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-theme-border gap-4">
            <button
              onClick={handleComplete}
              className="text-xs font-semibold text-theme-subtle hover:text-theme-text transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-theme-accent rounded px-2 py-1 cursor-pointer"
            >
              Skip onboarding
            </button>
            <Button
              onClick={handleComplete}
              icon={ArrowRight}
            >
              Enter Workspace
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
