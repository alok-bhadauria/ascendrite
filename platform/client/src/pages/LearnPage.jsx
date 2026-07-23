import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { BookOpen, Lock, Unlock, CheckCircle2, Clock, ArrowRight, Sparkles, ChevronRight } from 'lucide-react';
import { Button } from '../components/primitives/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Badge } from '../components/primitives/Badge';
import { useAuthStore } from '../store/authStore';

// Mock curriculum roadmap pipelines for each primary interest track
const curriculumData = {
  'ai': {
    title: 'Artificial Intelligence Pathway',
    description: 'Master convolutional networks, deep learning layers, and agent optimization parameters.',
    modules: [
      {
        id: 'ml-foundations',
        title: 'Machine Learning Foundations',
        description: 'Linear regressions, gradient descents, loss parameters, and error fitting calculations.',
        unlocked: true,
        completed: true,
        duration: '45m',
        difficulty: 'Medium',
        topics: ['Gradient Descent Derivations', 'MSE Cost Fit', 'Overfitting Optimization']
      },
      {
        id: 'deep-learning',
        title: 'Deep Learning Networks',
        description: 'Multi-layer feed-forward networks, backpropagation calculus, and weights updates.',
        unlocked: true,
        completed: false,
        duration: '60m',
        difficulty: 'Hard',
        topics: ['Backpropagation Chain Rule', 'Activation Functions (ReLU, Sigmoid)', 'Weights & Biases Mapping']
      },
      {
        id: 'multi-agents',
        title: 'Multi-Agent Architectures',
        description: 'Orchestrating autonomous agents, communication paradigms, and tool capabilities.',
        unlocked: false,
        completed: false,
        duration: '75m',
        difficulty: 'Expert',
        topics: ['Agent Coordination Protocols', 'Execution Tree Planning', 'Context Allocation Limits']
      }
    ]
  },
  'core-cs': {
    title: 'Core Computer Science Pathway',
    description: 'Build low-level systems, thread executors, database index parameters, and networks.',
    modules: [
      {
        id: 'dbms-engines',
        title: 'DBMS Database Engines',
        description: 'Relational storage engines, locking schemas, and index tree traversals.',
        unlocked: true,
        completed: true,
        duration: '40m',
        difficulty: 'Medium',
        topics: ['B-Tree Index Traversals', 'ACID Transactions Isolation', 'Query Execution Planners']
      },
      {
        id: 'os-threads',
        title: 'Operating Systems & Threads',
        description: 'Thread scheduling, CPU registers, process execution bounds, and locks.',
        unlocked: true,
        completed: false,
        duration: '50m',
        difficulty: 'Hard',
        topics: ['Mutex & Semaphores', 'CPU Thread Context Switching', 'Memory Mappings']
      },
      {
        id: 'computer-networking',
        title: 'Computer Networking Protocols',
        description: 'TCP handshakes, UDP framing, multiplexing, and routing logic.',
        unlocked: false,
        completed: false,
        duration: '60m',
        difficulty: 'Medium',
        topics: ['TCP Congestion Controls', 'Multiplexing HTTP/3', 'Routing Gateways Mappings']
      }
    ]
  },
  'software-engineering': {
    title: 'Software Engineering Pathway',
    description: 'Object-oriented structures, robust architectural components, and system design layouts.',
    modules: [
      {
        id: 'oop-design',
        title: 'Object-Oriented System Design',
        description: 'SOLID patterns, separation of domain rules, and class encapsulation.',
        unlocked: true,
        completed: true,
        duration: '35m',
        difficulty: 'Medium',
        topics: ['SOLID Code Design', 'Dependency Injections', 'Encapsulation Limits']
      },
      {
        id: 'scalable-architecture',
        title: 'Scalable System Architecture',
        description: 'Microservices configuration, load balancers, caching, and backups.',
        unlocked: true,
        completed: false,
        duration: '55m',
        difficulty: 'Hard',
        topics: ['Load Balancer Rules', 'Write-Through Caching', 'Database Sharding Patterns']
      },
      {
        id: 'clean-code-refactoring',
        title: 'Clean Code & Refactoring',
        description: 'Code smell analysis, test-driven development, and modular architecture validation.',
        unlocked: false,
        completed: false,
        duration: '45m',
        difficulty: 'Medium',
        topics: ['Unit Testing Mocking', 'Refactoring Code Smells', 'Integration Verification Gates']
      }
    ]
  },
  'web-development': {
    title: 'Web Development Pathway',
    description: 'Full-stack client configurations, state synchronizers, and REST API frameworks.',
    modules: [
      {
        id: 'html-css-git',
        title: 'Web Core Layouts & Git',
        description: 'Semantic HTML structures, flexbox alignments, responsive layout models, and branches.',
        unlocked: true,
        completed: true,
        duration: '30m',
        difficulty: 'Easy',
        topics: ['Semantic Document Landmarks', 'Responsive Media Queries', 'Git Branches & Tags Merges']
      },
      {
        id: 'reactjs-vite',
        title: 'Component State & Vite Bundler',
        description: 'React dynamic properties, hooks, state lifecycle, and bundler compiling.',
        unlocked: true,
        completed: false,
        duration: '50m',
        difficulty: 'Medium',
        topics: ['React hooks states rules', 'Vite configuration targets', 'Single page routing layouts']
      },
      {
        id: 'expressjs-mongodb',
        title: 'Backend API Frameworks',
        description: 'Express controllers, dynamic route parameters, and MongoDB data mapping.',
        unlocked: false,
        completed: false,
        duration: '60m',
        difficulty: 'Hard',
        topics: ['REST endpoint routing parameters', 'Database document storage mapping', 'Capabilities token authorization']
      }
    ]
  }
};

export default function LearnPage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const trackInterest = user?.preferences?.interest || 'web-development';
  const pathway = curriculumData[trackInterest] || curriculumData['web-development'];

  // Calculate progress details
  const totalModules = pathway.modules.length;
  const completedModules = pathway.modules.filter(m => m.completed).length;
  const progressPercent = Math.round((completedModules / totalModules) * 100);

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
          {pathway.modules.map((mod, idx) => {
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
