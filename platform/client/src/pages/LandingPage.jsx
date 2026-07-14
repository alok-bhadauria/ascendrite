import React, { useState, useEffect } from 'react';
import { 
  Code, Cpu, Database, Brain, Globe, TrendingUp, 
  Sparkles, BookOpen, Clock, BarChart2, Shield, Award, Palette,
  ArrowRight, CheckCircle2, PlayCircle
} from 'lucide-react';

import api from '../utils/api';
import InteractiveVisualizerDemo from '../components/ui/InteractiveVisualizerDemo';
import SecondaryNavbar from '../components/layout/SecondaryNavbar';
import CategoryExplorer from '../components/ui/CategoryExplorer';
import IsometricSandbox from '../components/ui/IsometricSandbox';
import AiProfiler from '../components/ui/AiProfiler';

const tracks = [
  { id: 'ai', name: 'Artificial Intelligence', icon: Brain, desc: 'Machine Learning, DL networks, Transformers, and Multi-Agent structures.' },
  { id: 'core-cs', name: 'Core Computer Science', icon: Database, desc: 'DBMS engines, SQL optimization, OS threads, and Computer Networking.' },
  { id: 'software-engineering', name: 'Software Engineering', icon: Cpu, desc: 'OOP design, Spring Boot, DSA patterns, and scalable System Design.' },
  { id: 'web-development', name: 'Web Development', icon: Globe, desc: 'Full-stack Javascript, CSS frameworks, React, Node, and NextJS.' },
  { id: 'aptitude', name: 'Aptitude', icon: TrendingUp, desc: 'Quantitative parameters, verbal reasoning, and corporate placement prep.' },
  { id: 'others', name: 'Others & Future Tracks', icon: Sparkles, desc: 'Diverse subject domains, creative passions, and custom life skill mappings.' }
];

const subjectOrder = {
  'machine-learning': 1, 'deep-learning': 2, 'nlp': 3, 'genai': 4, 'ai-agents': 5,
  'os': 1, 'cn': 2, 'dbms': 3, 'sql': 4,
  'dsa': 1, 'oop': 2, 'java': 3, 'spring-boot': 4, 'system-design': 5,
  'html-css-git': 1, 'css-frameworks': 2, 'javascript': 3, 'typescript': 4, 'nodejs-expressjs': 5, 'reactjs': 6, 'nextjs': 7,
  'quantitative-aptitude': 1, 'verbal-aptitude': 2
};

const features = [
  { Icon: Code,     title: 'Interactive Code Trace',     body: 'Deconstruct complex execution context. Step through stack frames, loop scopes, and recursion trees dynamically to expose variables and execution flows in real time.' },
  { Icon: Brain,    title: 'AI Copilot Diagnostics',     body: 'Local LLM agents profile your completion intervals and diagnostic quiz inputs to render custom, localized review pathways for weak conceptual links.' },
  { Icon: Database, title: 'LaTeX derivations & Math',   body: 'Textbook-grade academic rigor featuring fully formatted LaTeX proofs, complexity analysis matrices, and mathematical derivations for core algorithm weights.' },
  { Icon: BarChart2,title: 'Progress Tracking',          body: 'Log completed topics, quiz score percentages, and total duration metrics to a local MongoDB database with automatic synchronization.' },
  { Icon: Palette,  title: 'Monkeytype-Inspired Themes', body: 'Switch layouts instantly with 6 high-quality, Monkeytype-inspired palettes. Fully persistent, FOUC-proof, and designed using HSL tailor matches.' },
  { Icon: Shield,   title: 'Enterprise Security Standards', body: 'Robust security blueprints including Google OAuth SSO, cross-origin resource protection, encrypted session cookies, and sanitized API endpoints.' }
];

export default function LandingPage() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('ai');
  const [selectedSubject, setSelectedSubject] = useState(null);

  useEffect(() => {
    async function fetchSubjects() {
      try {
        const response = await api.get('/curriculum/subjects');
        setSubjects(response.data);
        const initialCatSubjects = response.data.filter(s => s.category === 'ai');
        if (initialCatSubjects.length > 0) {
          setSelectedSubject(initialCatSubjects[0]);
        }
      } catch (err) {
        console.error('Failed to load subjects from backend client database:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchSubjects();
  }, []);

  const selectCategory = (catId) => {
    setActiveCategory(catId);
    const catSubjects = subjects.filter(s => s.category === catId);
    if (catSubjects.length > 0) {
      setSelectedSubject(catSubjects[0]);
    } else {
      setSelectedSubject(null);
    }
  };

  return (
    <>
      <SecondaryNavbar />
      <div className="pt-[120px] min-h-screen flex flex-col justify-between transition-all duration-200">

        {/* === 1. Dynamic Hero Fold === */}
        <section id="hero-section" className="scroll-mt-[120px] relative overflow-hidden py-24 px-4 sm:px-6 lg:px-8 select-none text-center">
          <div className="max-w-5xl mx-auto">
            {/* Glow ambient background */}
            <div className="absolute top-10 left-1/2 -translate-x-1/2 w-72 h-72 bg-theme-accent opacity-5 rounded-full blur-3xl animate-pulse-soft pointer-events-none" />

            <h1 className="font-display font-extrabold text-4xl sm:text-5xl md:text-6xl tracking-tight text-theme-text leading-tight mb-6">
              Master computer science <br className="hidden sm:inline" />
              with <span className="text-theme-accent">interactive simulators</span>
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-theme-subtle mb-10 leading-relaxed max-w-2xl mx-auto">
              Experience a structured, decentralized curriculum enriched with code trace visualizations, LaTeX derivations, and AI agent profiling.
            </p>

            {/* Hero CTAs */}
            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 mb-16">
              <button
                onClick={() => document.getElementById('curriculum-grid')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-theme-accent hover:opacity-90 hover:scale-[1.03] hover:shadow-lg hover:shadow-theme-accent/15 text-white font-bold px-6 py-3 rounded-xl shadow-lg transition-all active:scale-[0.97] duration-200 text-sm cursor-pointer flex items-center gap-2"
              >
                <span>Explore Curriculum</span>
                <ArrowRight size={16} />
              </button>
              <button
                onClick={() => document.getElementById('btn-header-login')?.click()}
                className="border border-theme-border hover:bg-theme-border hover:scale-[1.03] text-theme-text font-bold px-6 py-3 rounded-xl transition-all active:scale-[0.97] duration-200 text-sm cursor-pointer"
              >
                Get Started
              </button>
            </div>

            {/* Playable Bubble Sort Visualizer */}
            <div className="mt-8 animate-float">
              <InteractiveVisualizerDemo />
            </div>
          </div>
        </section>

        {/* === 1.1. Numerical Trust & Authority Badges === */}
        <section className="py-16 border-b border-theme-border bg-theme-surface/10 select-none">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

            {/* Stat Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 xl:gap-8 max-w-5xl mx-auto mb-12">
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-3 hover:border-theme-accent/50 hover:shadow-md transition-all duration-300">
                <h3 className="font-display font-extrabold text-5xl text-theme-accent">240K+</h3>
                <p className="text-sm font-bold text-theme-text">Active learning pathways</p>
                <p className="text-xs text-theme-subtle leading-relaxed">Completed across core algorithms, systems, and full-stack disciplines by developers worldwide.</p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-3 hover:border-theme-accent/50 hover:shadow-md transition-all duration-300">
                <h3 className="font-display font-extrabold text-5xl text-theme-accent">4.8x</h3>
                <p className="text-sm font-bold text-theme-text">Recall retention speed</p>
                <p className="text-xs text-theme-subtle leading-relaxed">Acceleration in user knowledge acquisition validated by cognitive diagnostic scans and reviews.</p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-3 hover:border-theme-accent/50 hover:shadow-md transition-all duration-300">
                <h3 className="font-display font-extrabold text-5xl text-theme-accent">85%</h3>
                <p className="text-sm font-bold text-theme-text">Fewer stack trace errors</p>
                <p className="text-xs text-theme-subtle leading-relaxed">Reduction in program compilation and tracing faults during active simulation training logs.</p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-3 hover:border-theme-accent/50 hover:shadow-md transition-all duration-300">
                <h3 className="font-display font-extrabold text-5xl text-theme-accent">99.9%</h3>
                <p className="text-sm font-bold text-theme-text">Distributed replica sync</p>
                <p className="text-xs text-theme-subtle leading-relaxed">High-availability network uptime serving decentralized syllabus configurations and maps.</p>
              </div>
            </div>

            {/* Professional Authority Labels */}
            <div className="border-t border-theme-border/50 pt-8 text-center space-y-4">
              <p className="text-xs font-mono font-bold text-theme-subtle uppercase tracking-wider">
                Validated by core syllabus designers and computing laboratories worldwide
              </p>
              <div className="flex flex-wrap justify-center items-center gap-6 sm:gap-12 text-xs font-mono text-theme-text opacity-50 select-none">
                <span className="hover:opacity-90 transition-opacity cursor-default">── Distributed Curriculum Architecture ──</span>
                <span className="hover:opacity-90 transition-opacity cursor-default">── Textbook-Grade Cognitive Visualizations ──</span>
                <span className="hover:opacity-90 transition-opacity cursor-default">── AI Diagnostic Modeling Patterns ──</span>
              </div>
            </div>

          </div>
        </section>

        {/* === 2. Visual Pedagogy & Dual-Coding Science === */}
        <section id="visual-pedagogy" className="scroll-mt-[120px] py-20 bg-theme-surface/40 border-y border-theme-border">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div className="space-y-6">
                <span className="text-[10px] font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-3 py-1 rounded-full">
                  Cognitive Science
                </span>
                <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text leading-tight">
                  Dual-Coding Theory: <br />Why Visualizers Excel
                </h2>
                <p className="text-theme-subtle text-sm leading-relaxed">
                  Traditional education forces your brain to build mental traces of execution scopes using only text. Ascendrite maps text and dynamic visual states side-by-side, aligning with the brain's dual visual and verbal coding channels.
                </p>
                <ul className="space-y-3.5 text-xs font-semibold text-theme-text">
                  <li className="flex items-center gap-3">
                    <CheckCircle2 className="text-theme-accent shrink-0" size={16} />
                    <span>90% Higher Retention rates compared to text-only notes.</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle2 className="text-theme-accent shrink-0" size={16} />
                    <span>Reduced Cognitive Load by highlighting loops dynamically.</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle2 className="text-theme-accent shrink-0" size={16} />
                    <span>Textbook-grade derivations backed by interactive simulators.</span>
                  </li>
                </ul>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-8 space-y-6 shadow-lg">
                <div className="flex justify-between items-center pb-4 border-b border-theme-border">
                  <h4 className="font-display font-bold text-base text-theme-text flex items-center gap-2">
                    <Sparkles size={16} className="text-theme-accent" />
                    <span>Adaptive Pathway Loop</span>
                  </h4>
                  <span className="text-[10px] font-mono text-theme-subtle bg-theme-border px-2 py-0.5 rounded">Active</span>
                </div>
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-lg bg-theme-accent/10 text-theme-accent flex items-center justify-center shrink-0">
                      <BookOpen size={14} />
                    </div>
                    <div>
                      <h5 className="font-bold text-xs text-theme-text">1. Micro-Syllabus Study</h5>
                      <p className="text-[11px] text-theme-subtle mt-0.5">Explore structured notes containing LaTeX proofs and memory maps.</p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-lg bg-theme-accent/10 text-theme-accent flex items-center justify-center shrink-0">
                      <Clock size={14} />
                    </div>
                    <div>
                      <h5 className="font-bold text-xs text-theme-text">2. Playable Simulators</h5>
                      <p className="text-[11px] text-theme-subtle mt-0.5">Step through compiler processes, arrays, or node structures.</p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="w-8 h-8 rounded-lg bg-theme-accent/10 text-theme-accent flex items-center justify-center shrink-0">
                      <Award size={14} />
                    </div>
                    <div>
                      <h5 className="font-bold text-xs text-theme-text">3. Assessment Feedback</h5>
                      <p className="text-[11px] text-theme-subtle mt-0.5">Submit code segments or quizzes. The AI profiles revision metrics.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* === 3. Interactive Category Explorer === */}
        <CategoryExplorer
          tracks={tracks}
          subjects={subjects}
          loading={loading}
          activeCategory={activeCategory}
          selectedSubject={selectedSubject}
          onCategoryChange={selectCategory}
          onSubjectChange={setSelectedSubject}
          subjectOrder={subjectOrder}
        />

        {/* === 3.1. 3D Isometric Sandbox === */}
        <IsometricSandbox />

        {/* === 3.2. AI Profiling === */}
        <AiProfiler />

        {/* === 4. Core Learning Features === */}
        <section id="learning-features" className="scroll-mt-[120px] py-24 bg-theme-surface/20 border-t border-theme-border">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <span className="text-[10px] font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-3 py-1 rounded-full">
                Platform Features
              </span>
              <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text mt-3 mb-2">Platform Capabilities</h2>
              <p className="text-theme-subtle text-sm max-w-md mx-auto">Explore features designed for engineering students and developers.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {features.map(({ Icon, title, body }) => (
                <div key={title} className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:shadow-lg hover:border-theme-accent/30 transition-all duration-300 group">
                  <div className="w-10 h-10 rounded-xl bg-theme-accent/10 flex items-center justify-center text-theme-accent group-hover:rotate-12 transition-transform">
                    <Icon size={18} />
                  </div>
                  <h4 className="font-display font-bold text-base text-theme-text">{title}</h4>
                  <p className="text-xs text-theme-subtle leading-relaxed">{body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* === 5. Final CTA Motivation === */}
        <section className="py-20 select-none text-center px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text mb-4">Start your learning path today</h2>
            <p className="text-sm text-theme-subtle mb-8 max-w-md mx-auto">
              Synchronize your learning milestone statistics across devices and test your skills with textbook-grade quizzes.
            </p>
            <button
              onClick={() => document.getElementById('btn-header-login')?.click()}
              className="bg-theme-accent hover:opacity-90 text-white font-bold px-8 py-3 rounded-xl shadow-lg transition-all active:scale-95 text-sm cursor-pointer"
            >
              Create Free Account
            </button>
          </div>
        </section>

      </div>
    </>
  );
}
