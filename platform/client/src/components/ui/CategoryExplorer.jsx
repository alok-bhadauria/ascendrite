import React from 'react';
import { PlayCircle } from 'lucide-react';
import SubjectVisualizer from './SubjectVisualizer';

/**
 * CategoryExplorer renders the interactive curriculum roadmap grid.
 * It displays the subject category sidebar, the subject timeline,
 * and the dynamic subject visualizer preview.
 */
export default function CategoryExplorer({
  tracks,
  subjects,
  loading,
  activeCategory,
  selectedSubject,
  onCategoryChange,
  onSubjectChange,
  subjectOrder
}) {
  const currentCategorySubjects = subjects
    .filter(s => s.category === activeCategory)
    .sort((a, b) => {
      const orderA = subjectOrder[a.subject_id] || 99;
      const orderB = subjectOrder[b.subject_id] || 99;
      return orderA - orderB;
    });

  return (
    <section id="curriculum-grid" className="scroll-mt-[120px] py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-xs font-mono text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-3 py-1 rounded-full">
            Knowledge Hub
          </span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text mt-3 mb-2">Dynamic Knowledge Roadmap Tree</h2>
          <p className="text-theme-subtle text-sm max-w-md mx-auto">Click through subject pipelines to trigger direct compilation and diagram simulations.</p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-8 h-8 rounded-full border-4 border-theme-border border-t-theme-accent animate-spin" />
            <p className="text-xs text-theme-subtle font-semibold">Loading syllabus roadmap configurations...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start max-w-6xl mx-auto">
            
            {/* Left Nav: Subject Categories */}
            <div className="lg:col-span-3 flex flex-col gap-2">
              <h4 className="font-display font-bold text-xs text-theme-subtle uppercase tracking-wider mb-2 px-1">Subject Areas</h4>
              {tracks.map(t => {
                const Icon = t.icon;
                const isActive = activeCategory === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => onCategoryChange(t.id)}
                    className={`w-full text-left p-3.5 rounded-xl border transition-all duration-300 flex items-center gap-3 cursor-pointer ${
                      isActive 
                        ? 'bg-theme-surface border-theme-accent shadow-md scale-[1.01]' 
                        : 'border-theme-border/60 hover:bg-theme-surface/50'
                    }`}
                  >
                    <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                      isActive ? 'bg-theme-accent text-white' : 'bg-theme-border text-theme-text'
                    }`}>
                      <Icon size={14} />
                    </div>
                    <span className="font-display font-bold text-sm text-theme-text">{t.name}</span>
                  </button>
                );
              })}
            </div>

            {/* Right Display: Nested Connected Pipeline Card */}
            {activeCategory === 'others' ? (
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-4 sm:p-6 md:p-8 shadow-xl grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch min-h-[440px] animate-fade-in">
                {/* Left Side: Category Blocks */}
                <div className="flex flex-col justify-between space-y-6">
                  <div>
                    <span className="text-xs font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-2.5 py-1 rounded-full select-none">
                      Expanding Knowledge Frontiers
                    </span>
                    <h3 className="font-display font-extrabold text-2xl text-theme-text mt-4 leading-tight">
                      Scaling to cover all interests and skills
                    </h3>
                    <p className="text-sm text-theme-subtle mt-2 leading-relaxed">
                      Ascendrite is dynamically mapping structured syllabus graphs across creative, scientific, and vocational disciplines—each matching the same rich double-coding simulations.
                    </p>
                  </div>
                  
                  {/* Grid of future tracks */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl space-y-1">
                      <span className="font-bold text-theme-accent block font-display">Creative Passions</span>
                      <span className="text-[10px] text-theme-subtle block">Photography, Film &amp; Editing, Sound Design</span>
                    </div>
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl space-y-1">
                      <span className="font-bold text-[#10b981] block font-display">Applied Sciences</span>
                      <span className="text-[10px] text-theme-subtle block">Cosmology, Geology, Medical Diagnostics</span>
                    </div>
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl space-y-1">
                      <span className="font-bold text-[#f59e0b] block font-display">Life Vocation</span>
                      <span className="text-[10px] text-theme-subtle block">Personal Finance, Rhetoric, Survival Camping</span>
                    </div>
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl space-y-1">
                      <span className="font-bold text-[#8b5cf6] block font-display">Human Behaviour</span>
                      <span className="text-[10px] text-theme-subtle block">Cognitive Psychology, Sociology, Analytics</span>
                    </div>
                  </div>
                </div>

                {/* Right Side: Expanding Universe SVG Node Tree */}
                <div className="bg-theme-bg border border-theme-border rounded-2xl p-6 flex flex-col justify-center items-center relative overflow-hidden shadow-inner min-h-[300px]">
                  <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2 absolute top-4">Syllabus Expansion DAG</span>
                  <svg className="w-full h-48 fill-none stroke-theme-accent mt-6" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="8" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="2" />
                    <circle cx="20" cy="20" r="5" fill="#10b981" />
                    <circle cx="80" cy="20" r="5" fill="var(--color-theme-accent)" />
                    <circle cx="20" cy="80" r="5" fill="#f59e0b" />
                    <circle cx="80" cy="80" r="5" fill="#8b5cf6" />
                    <line x1="50" y1="50" x2="20" y2="20" stroke="var(--color-theme-accent)" strokeWidth="1" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="80" y2="20" stroke="var(--color-theme-accent)" strokeWidth="1" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="20" y2="80" stroke="var(--color-theme-accent)" strokeWidth="1" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="80" y2="80" stroke="var(--color-theme-accent)" strokeWidth="1" strokeDasharray="3" />
                    <text x="43" y="53" fill="var(--color-theme-text)" fontSize="8" fontWeight="bold">Root</text>
                  </svg>
                  <span className="text-xs font-mono text-theme-subtle text-center pb-2">Continuously compiling active nodes...</span>
                </div>
              </div>
            ) : (
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-4 sm:p-6 md:p-8 shadow-xl grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch min-h-[440px]">
                
                {/* Connected Subject Details & Timeline */}
                <div className="flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-2.5 py-1 rounded-full select-none">
                      {activeCategory.replace("-", " ")} Pipeline
                    </span>
                    
                    <div className="mt-6 pl-4 relative space-y-4">
                      {/* Vertical timeline connector line */}
                      <div className="absolute left-[3px] top-4 bottom-4 w-0.5 bg-theme-border" />
                      
                      {currentCategorySubjects.map((sub) => {
                        const isSelected = selectedSubject?.subject_id === sub.subject_id;
                        return (
                          <button
                            key={sub.subject_id}
                            onClick={() => onSubjectChange(sub)}
                            className="flex items-start gap-4 text-left w-full relative z-10 group cursor-pointer focus:outline-none"
                          >
                            {/* Left node indicator */}
                            <div className={`w-2 h-2 rounded-full border-2 mt-1.5 transition-all duration-300 shrink-0 ${
                              isSelected 
                                ? 'bg-theme-accent border-theme-bg scale-125 ring-4 ring-theme-accent/25' 
                                : 'bg-theme-bg border-theme-subtle group-hover:border-theme-accent'
                            }`} />
                            
                            <div className="flex-1">
                              <h5 className={`font-display font-bold text-base leading-tight transition-colors ${
                                isSelected ? 'text-theme-accent font-extrabold' : 'text-theme-text group-hover:text-theme-accent font-bold'
                              }`}>
                                {sub.name}
                              </h5>
                              {isSelected && (
                                <p className="text-sm text-theme-subtle mt-1.5 leading-relaxed transition-all animate-fade-in">
                                  {sub.metadata?.description || "High-end pipeline syllabus mapping core derivations, LaTeX equations, and execution blocks."}
                                </p>
                              )}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {selectedSubject && (
                    <button
                      onClick={() => alert(`Starting pathway: ${selectedSubject.name}`)}
                      className="w-full mt-6 bg-theme-accent hover:opacity-90 hover:scale-[1.02] hover:shadow-md hover:shadow-theme-accent/15 text-white font-bold py-2.5 rounded-xl transition-all shadow-md active:scale-[0.98] duration-200 flex items-center justify-center gap-2 cursor-pointer text-xs"
                    >
                      <PlayCircle size={14} />
                      <span>Start learning path</span>
                    </button>
                  )}
                </div>

                {/* Dynamic Interactive Render Sandbox Preview */}
                <div className="bg-theme-bg border border-theme-border rounded-2xl p-6 flex flex-col items-stretch justify-center relative overflow-hidden shadow-inner min-h-[300px]">
                  <SubjectVisualizer selectedSubject={selectedSubject} />
                </div>

              </div>
            )}

          </div>
        )}
      </div>
    </section>
  );
}
