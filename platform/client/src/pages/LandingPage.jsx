import React, { useState, useEffect } from 'react';
import { FaCode, FaRobot, FaDatabase, FaGraduationCap } from 'react-icons/fa';
import api from '../utils/api';
import InteractiveVisualizerDemo from '../components/ui/InteractiveVisualizerDemo';

export default function LandingPage() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    async function fetchSubjects() {
      try {
        const response = await api.get('/curriculum/subjects');
        setSubjects(response.data);
      } catch (err) {
        console.error('Failed to load subjects from backend client database:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchSubjects();
  }, []);

  const categories = [
    { id: 'all', name: 'All Subjects' },
    { id: 'ai', name: 'Artificial Intelligence' },
    { id: 'core-cs', name: 'Core CS' },
    { id: 'software-engineering', name: 'Software Engineering' },
    { id: 'web-development', name: 'Web Development' },
    { id: 'aptitude', name: 'Aptitude' }
  ];

  const filteredSubjects = activeCategory === 'all'
    ? subjects
    : subjects.filter(s => s.category === activeCategory);

  return (
    <div className="pt-24 min-h-screen flex flex-col justify-between transition-all duration-200">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex-1 py-8">
        
        {/* Dynamic Hero Section */}
        <section className="text-center max-w-4xl mx-auto mb-20 select-none">
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl md:text-6xl tracking-tight text-theme-text leading-tight mb-6">
            Master computer science <br className="hidden sm:inline" />
            with <span className="text-theme-accent">interactive simulators</span>
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-theme-subtle mb-10 leading-relaxed max-w-2xl mx-auto">
            Experience a structured, decentralized curriculum enriched with code trace visualizations, LaTeX derivations, and AI agent profiling.
          </p>
          
          {/* Hero CTAs */}
          <div className="flex justify-center gap-4 mb-16">
            <button 
              onClick={() => {
                const element = document.getElementById('curriculum-grid');
                element?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="bg-theme-accent hover:opacity-90 text-white font-bold px-6 py-3 rounded-xl shadow-lg transition-all active:scale-95 text-base cursor-pointer"
            >
              Explore Curriculum
            </button>
            <button 
              onClick={() => document.getElementById('btn-header-login')?.click()}
              className="border border-theme-border hover:bg-theme-border text-theme-text font-bold px-6 py-3 rounded-xl transition-all active:scale-95 text-base cursor-pointer"
            >
              Get Started
            </button>
          </div>

          {/* Interactive Sorting Simulator Demonstration */}
          <div className="mt-8 animate-float">
            <InteractiveVisualizerDemo />
          </div>
        </section>

        {/* Feature Grid Highlights */}
        <section className="mb-24">
          <div className="text-center mb-12">
            <h2 className="font-display font-bold text-3xl text-theme-text mb-2">Designed for engineering readiness</h2>
            <p className="text-theme-subtle max-w-md mx-auto text-sm">Every learning parameter is optimized to reduce cognitive load and build production capability.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {/* Feature Item 1 */}
            <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 hover:shadow-xl hover:scale-[1.02] hover:border-theme-accent transition-all duration-300">
              <div className="w-10 h-10 rounded-lg bg-theme-accent bg-opacity-15 flex items-center justify-center text-theme-accent mb-4">
                <FaCode size={18} />
              </div>
              <h3 className="font-display font-bold text-lg text-theme-text mb-2">Dynamic Code Trace</h3>
              <p className="text-xs text-theme-subtle leading-relaxed">
                Step through algorithm execution line-by-line while watching system memory bars morph dynamically.
              </p>
            </div>
            
            {/* Feature Item 2 */}
            <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 hover:shadow-xl hover:scale-[1.02] hover:border-theme-accent transition-all duration-300">
              <div className="w-10 h-10 rounded-lg bg-theme-accent bg-opacity-15 flex items-center justify-center text-theme-accent mb-4">
                <FaRobot size={18} />
              </div>
              <h3 className="font-display font-bold text-lg text-theme-text mb-2">Adaptive AI Tutoring</h3>
              <p className="text-xs text-theme-subtle leading-relaxed">
                Connect learning milestones with specialized LLM architectures and RAG pipelines for personalized help.
              </p>
            </div>
            
            {/* Feature Item 3 */}
            <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 hover:shadow-xl hover:scale-[1.02] hover:border-theme-accent transition-all duration-300">
              <div className="w-10 h-10 rounded-lg bg-theme-accent bg-opacity-15 flex items-center justify-center text-theme-accent mb-4">
                <FaDatabase size={18} />
              </div>
              <h3 className="font-display font-bold text-lg text-theme-text mb-2">Decentralized Syllabus</h3>
              <p className="text-xs text-theme-subtle leading-relaxed">
                Course modules index directly from decoupled JSON schema models mapping complexity analysis datasets.
              </p>
            </div>
          </div>
        </section>

        {/* Live Syllabus Directory */}
        <section id="curriculum-grid" className="scroll-mt-24 mb-16">
          <div className="text-center mb-10">
            <h2 className="font-display font-bold text-3xl text-theme-text mb-2">Decentralized Syllabus Directory</h2>
            <p className="text-theme-subtle text-sm">Browse subjects containing textbook-grade notes, mathematical derivations, and quizzes.</p>
          </div>

          {/* Filtering Categories Tabs */}
          <div className="flex flex-wrap gap-2 justify-center mb-10 select-none">
            {categories.map(cat => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`px-4 py-2 rounded-lg text-xs font-semibold tracking-wide transition-all border cursor-pointer ${
                  activeCategory === cat.id
                    ? 'bg-theme-accent border-theme-accent text-white shadow-md'
                    : 'border-theme-border text-theme-text hover:bg-theme-border'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>

          {/* Subjects Grid Area */}
          {loading ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3">
              <div className="w-8 h-8 rounded-full border-4 border-theme-border border-t-theme-accent animate-spin" />
              <p className="text-xs text-theme-subtle font-semibold">Loading live syllabus profiles index...</p>
            </div>
          ) : filteredSubjects.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
              {filteredSubjects.map(sub => (
                <div 
                  key={sub.subject_id} 
                  className="bg-theme-surface border border-theme-border rounded-xl p-5 shadow hover:shadow-lg hover:border-theme-accent transition-all duration-300 flex flex-col justify-between group"
                >
                  <div>
                    <span className="text-[10px] font-bold text-theme-accent uppercase tracking-wider bg-theme-accent bg-opacity-10 px-2.5 py-1 rounded-full">
                      {sub.category.replace("-", " ")}
                    </span>
                    <h3 className="font-display font-bold text-base text-theme-text mt-3 group-hover:text-theme-accent transition-all">
                      {sub.name}
                    </h3>
                    <p className="text-xs text-theme-subtle mt-2 line-clamp-2 leading-relaxed">
                      {sub.metadata?.description || 'Textbook-grade interactive curriculum with complexity metrics analysis.'}
                    </p>
                  </div>
                  <div className="mt-4 pt-3 border-t border-theme-border flex items-center justify-between">
                    <span className="text-[10px] font-mono text-theme-subtle">
                      {sub.modules?.length || 5} modules | {sub.modules?.reduce((acc, m) => acc + (m.topics?.length || 0), 0) || 25} topics
                    </span>
                    <span className="text-[10px] font-bold text-theme-accent opacity-0 group-hover:opacity-100 transition-all flex items-center gap-1">
                      Start &rarr;
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16 bg-theme-surface border border-theme-border rounded-xl max-w-md mx-auto">
              <FaGraduationCap size={44} className="mx-auto text-theme-subtle opacity-40 mb-3" />
              <p className="font-display font-bold text-base text-theme-text">No subjects found</p>
              <p className="text-xs text-theme-subtle mt-1">Check backend server logging connections or change filters.</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
