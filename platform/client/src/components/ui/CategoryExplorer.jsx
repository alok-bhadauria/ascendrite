import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Play, Compass, GitCommit } from 'lucide-react';

/**
 * CategoryExplorer renders the interactive curriculum roadmap.
 * Layout matches previous visual identity:
 * - Left column: Tracks Sidebar (Domain selection)
 * - Right column: Double-column layout containing:
 *   - Timeline of Subjects under active Category (Subject selection)
 *   - Interactive Modules and Concepts Tree mapping to start learning (Modules & Concepts selection)
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
  // Filter and sort subjects in the active category dynamically
  const currentCategorySubjects = subjects
    .filter(s => s.category === activeCategory)
    .sort((a, b) => {
      const orderA = subjectOrder[a.subject_id] || 99;
      const orderB = subjectOrder[b.subject_id] || 99;
      return orderA - orderB;
    });

  // Automatically select the first subject when active category changes
  useEffect(() => {
    if (currentCategorySubjects.length > 0 && !currentCategorySubjects.find(s => s.subject_id === selectedSubject?.subject_id)) {
      onSubjectChange(currentCategorySubjects[0]);
    }
  }, [activeCategory, subjects]);

  return (
    <section id="curriculum-grid" className="scroll-mt-[120px] py-24 select-none relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Title */}
        <div className="text-center mb-16">
          <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/10 border border-theme-accent/20 px-3.5 py-1 rounded-full">
            Knowledge Hub
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-theme-text mt-4 mb-2 tracking-tight">
            Interactive Curriculum Atlas
          </h2>
          <p className="text-theme-subtle text-sm max-w-md mx-auto leading-relaxed">
            Click through active tracks to trace compiler pathways, database engines, and structural concepts.
          </p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-8 h-8 rounded-full border-4 border-theme-border border-t-theme-accent animate-spin" />
            <p className="text-xs text-theme-subtle font-mono">Loading dynamic curriculum maps...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start max-w-6xl mx-auto">
            
            {/* 1. Left Nav: Category Selection Sidebar (Domain level) */}
            <div className="lg:col-span-3 flex flex-col gap-2">
              <h4 className="font-display font-bold text-[10px] text-theme-subtle uppercase tracking-wider mb-2 px-1">
                Syllabus Domains
              </h4>
              {tracks.map(t => {
                const Icon = t.icon;
                const isActive = activeCategory === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => onCategoryChange(t.id)}
                    className={`w-full text-left p-3.5 rounded-xl border transition-all duration-200 flex items-center gap-3 cursor-pointer select-none ${
                      isActive 
                        ? 'bg-theme-surface border-theme-accent shadow-md scale-[1.01]' 
                        : 'border-theme-border/60 hover:bg-theme-surface/50'
                    }`}
                  >
                    <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                      isActive ? 'bg-theme-accent text-white' : 'bg-theme-border text-theme-subtle'
                    }`}>
                      <Icon size={13} />
                    </div>
                    <span className="font-display font-bold text-sm text-theme-text">{t.name}</span>
                  </button>
                );
              })}
            </div>

            {/* 2. Right Display: Re-designed Dual Panel Map */}
            {activeCategory === 'others' || currentCategorySubjects.length === 0 ? (
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-6 sm:p-8 shadow-xl grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch min-h-[440px] animate-fade-in">
                
                {/* Left side: descriptions */}
                <div className="flex flex-col justify-between space-y-6">
                  <div>
                    <span className="text-xs font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-2.5 py-1 rounded-full">
                      Knowledge Frontier
                    </span>
                    <h3 className="font-display font-extrabold text-2xl text-theme-text mt-4 leading-tight">
                      Decentralized Curriculum Extension
                    </h3>
                    <p className="text-sm text-theme-subtle mt-2 leading-relaxed">
                      Ascendrite is dynamically curating detailed notes schemas and interactive visual environments for upcoming science and vocational fields.
                    </p>
                  </div>
                  
                  {/* Grid of future tracks */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl">
                      <span className="font-bold text-theme-accent block font-display">Creative Passions</span>
                      <span className="text-[10px] text-theme-subtle block mt-0.5">Film Editing, Sound Design</span>
                    </div>
                    <div className="bg-theme-bg border border-theme-border p-3 rounded-xl">
                      <span className="font-bold text-emerald-500 block font-display">Applied Sciences</span>
                      <span className="text-[10px] text-theme-subtle block mt-0.5">Cosmology, Medical Diagnostic</span>
                    </div>
                  </div>
                </div>

                {/* Right side: DAG Node SVG */}
                <div className="bg-theme-bg border border-theme-border rounded-2xl p-6 flex flex-col justify-center items-center relative overflow-hidden shadow-inner min-h-[300px]">
                  <span className="text-[10px] font-mono text-theme-accent uppercase font-bold text-center mt-2 absolute top-4">Syllabus Expansion DAG</span>
                  <svg className="w-full h-40 fill-none stroke-theme-accent mt-4" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="7" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
                    <circle cx="20" cy="20" r="4.5" fill="#10b981" />
                    <circle cx="80" cy="20" r="4.5" fill="var(--color-theme-accent)" />
                    <circle cx="20" cy="80" r="4.5" fill="#f59e0b" />
                    <circle cx="80" cy="80" r="4.5" fill="#8b5cf6" />
                    <line x1="50" y1="50" x2="20" y2="20" stroke="var(--color-theme-accent)" strokeWidth="0.75" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="80" y2="20" stroke="var(--color-theme-accent)" strokeWidth="0.75" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="20" y2="80" stroke="var(--color-theme-accent)" strokeWidth="0.75" strokeDasharray="3" />
                    <line x1="50" y1="50" x2="80" y2="80" stroke="var(--color-theme-accent)" strokeWidth="0.75" strokeDasharray="3" />
                    <text x="44" y="52.5" fill="var(--color-theme-text)" fontSize="7" fontWeight="bold">Root</text>
                  </svg>
                  <span className="text-[10px] font-mono text-theme-subtle text-center">Awaiting upstream consensus</span>
                </div>

              </div>
            ) : (
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-6 sm:p-8 shadow-xl grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch min-h-[460px] animate-fade-in">
                
                {/* 2.1 Timeline of Subjects under Category (Left panel inside Card) */}
                <div className="md:col-span-5 flex flex-col justify-between border-b md:border-b-0 md:border-r border-theme-border/60 pb-6 md:pb-0 md:pr-6">
                  <div>
                    <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-2.5 py-1 rounded-full select-none">
                      {activeCategory.replace("-", " ")} Pipeline
                    </span>
                    
                    <div className="mt-8 pl-4 relative space-y-5">
                      <div className="absolute left-[3px] top-4 bottom-4 w-0.5 bg-theme-border/50 border-dashed" />
                      
                      {currentCategorySubjects.map((sub) => {
                        const isSelected = selectedSubject?.subject_id === sub.subject_id;
                        return (
                          <button
                            key={sub.subject_id}
                            onClick={() => onSubjectChange(sub)}
                            className="flex items-start gap-4 text-left w-full relative z-10 group cursor-pointer focus:outline-none select-none"
                          >
                            <div className={`w-2.5 h-2.5 rounded-full border-2 mt-1.5 transition-all duration-300 shrink-0 ${
                              isSelected 
                                ? 'bg-theme-accent border-theme-bg scale-125 ring-4 ring-theme-accent/25' 
                                : 'bg-theme-bg border-theme-subtle group-hover:border-theme-accent'
                            }`} />
                            
                            <div className="flex-1">
                              <h5 className={`font-display font-bold text-sm leading-tight transition-colors ${
                                isSelected ? 'text-theme-accent font-extrabold' : 'text-theme-text group-hover:text-theme-accent font-bold'
                              }`}>
                                {sub.name}
                              </h5>
                              <div className="flex gap-2 text-[9px] font-mono text-theme-subtle mt-0.5">
                                <span>{sub.difficulty}</span>
                                <span>•</span>
                                <span>{sub.metadata?.estimated_hours || 40} hrs</span>
                              </div>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {selectedSubject && (
                    <Link
                      to={`/learn/${selectedSubject.modules?.[0]?.id || 'ml-foundations'}`}
                      className="w-full mt-8 bg-theme-accent hover:opacity-90 hover:scale-[1.01] hover:shadow-md hover:shadow-theme-accent/15 text-white font-bold py-2.5 rounded-xl transition-all shadow-md active:scale-[0.98] duration-200 flex items-center justify-center gap-2 cursor-pointer text-xs"
                    >
                      <Play size={12} fill="white" />
                      <span>Start learning path</span>
                    </Link>
                  )}
                </div>

                {/* 2.2 Interactive Syllabus Modules & Concepts (Right panel inside Card) */}
                <div className="md:col-span-7 flex flex-col justify-between">
                  {selectedSubject ? (
                    <div className="space-y-6">
                      <div className="flex justify-between items-center pb-3 border-b border-theme-border/50">
                        <span className="text-[10px] font-mono font-bold text-theme-subtle uppercase tracking-wider">
                          Syllabus Structure Nodes
                        </span>
                        <span className="text-[10px] font-mono text-theme-accent">
                          {selectedSubject.modules?.length || 0} Modules loaded
                        </span>
                      </div>

                      {/* Vertically scrolling Modules list */}
                      <div className="space-y-5 max-h-[300px] overflow-y-auto pr-2 relative">
                        {selectedSubject.modules?.map((mod, idx) => (
                          <div key={mod.id} className="space-y-2 border-l border-theme-border/50 pl-3 relative group">
                            <div className="absolute -left-[4.5px] top-1.5 w-2 h-2 rounded-full bg-theme-border group-hover:bg-theme-accent transition-colors" />
                            
                            <div className="flex items-center gap-2 text-[9px] font-mono">
                              <span className="text-theme-accent font-semibold">M0{idx + 1}</span>
                              <span className="text-theme-subtle">({mod.duration || '40m'})</span>
                            </div>
                            <h6 className="font-display font-bold text-xs text-theme-text leading-snug">
                              {mod.title}
                            </h6>
                            <p className="text-[11px] text-theme-subtle leading-relaxed">
                              {mod.description}
                            </p>

                            {/* Topics/Concepts mapping */}
                            <div className="flex flex-wrap gap-1.5 pt-1">
                              {mod.topics?.map(topic => (
                                <Link
                                  key={topic}
                                  to={`/learn/${mod.id}`}
                                  className="flex items-center gap-1 px-2 py-0.5 rounded bg-theme-bg/60 border border-theme-border hover:border-theme-accent/50 text-[9px] text-theme-text hover:text-theme-accent transition-colors"
                                >
                                  <GitCommit size={8} className="text-theme-accent" />
                                  <span>{topic}</span>
                                </Link>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-full text-center p-4">
                      <Compass size={24} className="text-theme-subtle/40 animate-spin-slow" />
                      <p className="text-xs text-theme-subtle font-mono mt-2">Select a subject pathway node</p>
                    </div>
                  )}

                  {selectedSubject && (
                    <div className="text-[9px] font-mono text-theme-subtle text-right border-t border-theme-border/30 pt-3 mt-4">
                      Path: Domain &gt; {selectedSubject.subject_id} &gt; active_modules
                    </div>
                  )}
                </div>

              </div>
            )}

          </div>
        )}
      </div>
    </section>
  );
}
