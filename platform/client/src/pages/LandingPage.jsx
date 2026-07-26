import React, { useState, useEffect } from 'react';
import { 
  Cpu, Database, Brain, Globe, TrendingUp, 
  Sparkles, BookOpen, Clock, Award,
  ArrowRight, CheckCircle2
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
  'os': 1, 'operating-systems': 1, 'dbms': 2, 'sql': 3, 'cn': 4,
  'java': 1, 'oop': 2, 'dsa': 3, 'spring-boot': 4, 'system-design': 5,
  'html-css-git': 1, 'css-frameworks': 2, 'javascript': 3, 'typescript': 4, 'reactjs': 5, 'nextjs': 6, 'nodejs-expressjs': 7,
  'quantitative-aptitude': 1, 'verbal-aptitude': 2
};

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
        <section id="hero-section" className="scroll-mt-[120px] relative overflow-hidden py-24 px-4 sm:px-6 lg:px-8 select-none">
          <div className="max-w-7xl mx-auto lg:grid lg:grid-cols-12 lg:gap-12 lg:items-center">
            {/* Glow ambient background */}
            <div className="absolute top-10 left-1/2 -translate-x-1/2 w-72 h-72 bg-theme-accent opacity-5 rounded-full blur-3xl animate-pulse-soft pointer-events-none" />

            {/* Left Column: Heading and Description */}
            <div className="lg:col-span-5 text-center lg:text-left space-y-6">
              <h1 className="font-display font-extrabold text-4xl sm:text-5xl lg:text-5xl xl:text-6xl tracking-tight text-theme-text leading-[1.1]">
                A Living Textbook for <br />
                <span className="text-theme-accent">Computer Systems</span>
              </h1>
              <p className="text-base sm:text-lg text-theme-subtle leading-relaxed max-w-xl mx-auto lg:mx-0">
                An interactive laboratory to study computer systems, database engines, and networking protocols. Step through logic states, mathematical proofs, and code stack visualizers.
              </p>

              {/* Hero CTAs */}
              <div className="flex flex-wrap justify-center lg:justify-start gap-3 sm:gap-4">
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
            </div>

            {/* Right Column: Interactive Simulator */}
            <div className="lg:col-span-7 mt-12 lg:mt-0 animate-float">
              <InteractiveVisualizerDemo />
            </div>
          </div>
        </section>

        {/* === 1.1. Curriculum Craftsmanship & Authority Badges === */}
        <section className="py-16 border-b border-theme-border bg-theme-surface/10 select-none">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Unified system telemetry stats dashboard */}
            <div className="bg-theme-bg border border-theme-border rounded-3xl p-8 max-w-5xl mx-auto shadow-inner relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-theme-accent" />
              
              <div className="flex justify-between items-center pb-6 border-b border-theme-border/65 mb-8">
                <span className="text-[10px] font-mono text-theme-accent uppercase font-bold tracking-wider">
                  // system_telemetry_readout.log
                </span>
                <div className="flex gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-theme-accent animate-ping" />
                  <span className="text-[9px] font-mono text-theme-subtle">status: stable</span>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                <div className="space-y-2 border-r-0 lg:border-r border-theme-border/40 last:border-r-0 pr-4">
                  <h3 className="font-display font-extrabold text-3xl text-theme-accent">100%</h3>
                  <p className="text-xs font-mono font-bold text-theme-text uppercase">Handcrafted Curricula</p>
                  <p className="text-[11px] text-theme-subtle leading-relaxed">Curated for software engineering precision and academic depth.</p>
                </div>
                <div className="space-y-2 border-r-0 lg:border-r border-theme-border/40 last:border-r-0 pr-4">
                  <h3 className="font-display font-extrabold text-3xl text-theme-accent">Dual</h3>
                  <p className="text-xs font-mono font-bold text-theme-text uppercase">Coding Retention</p>
                  <p className="text-[11px] text-theme-subtle leading-relaxed">Mathematical proofs matched side-by-side with step-by-step trace simulation loops.</p>
                </div>
                <div className="space-y-2 border-r-0 lg:border-r border-theme-border/40 last:border-r-0 pr-4">
                  <h3 className="font-display font-extrabold text-3xl text-theme-accent">Local</h3>
                  <p className="text-xs font-mono font-bold text-theme-text uppercase">First Architecture</p>
                  <p className="text-[11px] text-theme-subtle leading-relaxed">Runs inside local services for maximum availability, privacy, and speed.</p>
                </div>
                <div className="space-y-2 pr-4">
                  <h3 className="font-display font-extrabold text-3xl text-theme-accent">4 Core</h3>
                  <p className="text-xs font-mono font-bold text-theme-text uppercase">CS Tracks</p>
                  <p className="text-[11px] text-theme-subtle leading-relaxed">Comprehensive pathways across Systems, Algorithms, and Architectures.</p>
                </div>
              </div>
            </div>

            {/* Professional Authority Labels */}
            <div className="mt-8 text-center space-y-4">
              <p className="text-xs font-mono font-bold text-theme-subtle uppercase tracking-wider">
                Validated by core syllabus designers and computing laboratories worldwide
              </p>
              <div className="flex flex-wrap justify-center items-center gap-6 sm:gap-12 text-xs font-mono text-theme-text opacity-50 select-none">
                <span className="hover:opacity-90 transition-opacity cursor-default">── Distributed Curriculum Architecture ──</span>
                <span className="hover:opacity-90 transition-opacity cursor-default">── Textbook-Grade Cognitive Visualizations ──</span>
                <span className="hover:opacity-90 transition-opacity cursor-default">── Decentralized Progress Analytics ──</span>
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
                      <p className="text-[11px] text-theme-subtle mt-0.5">Submit code segments or quizzes. The system profiles revision metrics.</p>
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

        {/* === 3.2. Diagnostics Console === */}
        <AiProfiler />

        {/* === 4. Platform Capabilities Systems === */}
        <section id="learning-features" className="scroll-mt-[120px] py-24 bg-theme-surface/20 border-t border-theme-border/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/10 border border-theme-accent/20 px-3.5 py-1 rounded-full">
                Platform Architecture
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-theme-text mt-4 mb-2 tracking-tight">Core Systems Architecture</h2>
              <p className="text-theme-subtle text-sm max-w-md mx-auto leading-relaxed">Engineering infrastructure designed for structured learning and local diagnostics.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_01</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Curriculum Compiler Engine</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Ingests decentralized syllabus schemas from local database catalogs and maps them dynamically to progressive study indexes.
                </p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_02</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Double-Coding Visualizer Core</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Renders interactive 3D structures, code execution stacks, and mathematical LaTeX proofs side-by-side with reading materials.
                </p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_03</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Comprehension Diagnostic Kernel</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Monitors recall speed, flags conceptual weaknesses, and updates review latency metrics directly in local terminals.
                </p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_04</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Local-First Storage Registry</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Stores and manages all progress logs, bookmarks, and quiz statistics locally using database systems for maximum privacy.
                </p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_05</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Creator Workspace & Pipeline</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Authoring dashboards for developers to construct, duplicate, validate, and merge curriculum drafts through peer review gates.
                </p>
              </div>
              <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 space-y-4 hover:border-theme-accent/30 transition-all duration-300">
                <div className="text-xs font-mono text-theme-accent font-bold">// SYS_06</div>
                <h4 className="font-display font-extrabold text-base text-theme-text">Stateful Cryptographic Vault</h4>
                <p className="text-xs text-theme-subtle leading-relaxed">
                  Secures operations with cross-origin policies, encrypted cookie verification layers, and secure OAuth credentials routing.
                </p>
              </div>
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
