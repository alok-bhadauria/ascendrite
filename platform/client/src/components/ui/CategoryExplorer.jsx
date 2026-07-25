import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Play, Compass, Layers, 
  GitCommit, ChevronRight, Clock, HelpCircle 
} from 'lucide-react';

/**
 * CategoryExplorer renders the interactive curriculum roadmap grid.
 * It visualizes: Domain ➔ Subject ➔ Module ➔ Concept ➔ Learning Journey.
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

  // Filter subjects for the active category
  const currentCategorySubjects = subjects
    .filter(s => s.category === activeCategory)
    .sort((a, b) => {
      const orderA = subjectOrder[a.subject_id] || 99;
      const orderB = subjectOrder[b.subject_id] || 99;
      return orderA - orderB;
    });

  // Calculate stats for active track
  const totalHours = currentCategorySubjects.reduce((acc, s) => acc + (s.metadata?.estimated_hours || 40), 0);

  return (
    <section id="curriculum-grid" className="scroll-mt-[120px] py-24 select-none relative overflow-hidden">
      {/* Background spatial mesh decor */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* === Section Header === */}
        <div className="text-center mb-16">
          <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/10 border border-theme-accent/20 px-3.5 py-1 rounded-full">
            Knowledge Map
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-theme-text mt-4 mb-2 tracking-tight">
            Curriculum Topology Schema
          </h2>
          <p className="text-theme-subtle text-sm max-w-lg mx-auto leading-relaxed">
            Trace the structured pathways of engineering domains. Dive deep into modules, LaTeX proofs, and concepts nodes.
          </p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-8 h-8 rounded-full border-4 border-theme-border border-t-theme-accent animate-spin" />
            <p className="text-xs text-theme-subtle font-mono">Resolving metadata index cache...</p>
          </div>
        ) : (
          <div className="space-y-12">
            
            {/* === 1. Domain (Track) Bar === */}
            <div className="flex flex-wrap justify-center gap-2 max-w-4xl mx-auto">
              {tracks.map(t => {
                const Icon = t.icon;
                const isActive = activeCategory === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => onCategoryChange(t.id)}
                    className={`px-5 py-3 rounded-xl border transition-all duration-200 flex items-center gap-3 cursor-pointer select-none font-bold text-sm ${
                      isActive 
                        ? 'bg-theme-surface border-theme-accent text-theme-text shadow-md scale-[1.01]' 
                        : 'border-theme-border/50 bg-theme-surface/30 hover:bg-theme-surface hover:border-theme-border text-theme-subtle'
                    }`}
                  >
                    <Icon size={16} className={isActive ? 'text-theme-accent' : ''} />
                    <span>{t.name}</span>
                  </button>
                );
              })}
            </div>

            {/* === Empty & Upcoming State === */}
            {currentCategorySubjects.length === 0 ? (
              <div className="bg-theme-surface border border-theme-border rounded-3xl p-12 text-center max-w-3xl mx-auto space-y-6 shadow-xl">
                <Compass className="mx-auto text-theme-accent/40 animate-pulse-soft" size={48} />
                <h3 className="font-display font-bold text-xl text-theme-text"> frontier pipeline mapping active</h3>
                <p className="text-sm text-theme-subtle max-w-md mx-auto leading-relaxed">
                  The syllabus specifications for this track are currently being curated and validated against our engineering database schema. Dynamic nodes will ingest automatically.
                </p>
                <div className="pt-4 flex justify-center gap-4 text-xs font-mono text-theme-subtle">
                  <span>── Deployed: 4 Core tracks ──</span>
                  <span>── Under review: 2 Tracks ──</span>
                </div>
              </div>
            ) : (
              
              /* === 2. Connected Graph Canvas === */
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch max-w-6xl mx-auto">
                
                {/* Left Side: Subject Pipeline Nodes */}
                <div className="lg:col-span-4 flex flex-col gap-4">
                  <div className="flex justify-between items-center px-1 mb-2">
                    <span className="text-[10px] font-mono font-bold text-theme-subtle uppercase tracking-wider">
                      Subject Node list
                    </span>
                    <span className="text-[10px] font-mono text-theme-accent">
                      {totalHours} Total Hours Est.
                    </span>
                  </div>

                  <div className="space-y-3 relative">
                    {/* SVG Connector Flow line */}
                    <div className="absolute left-[24px] top-6 bottom-6 w-0.5 bg-theme-border/50 border-dashed" />

                    {currentCategorySubjects.map((sub, idx) => {
                      const isSelected = selectedSubject?.subject_id === sub.subject_id;
                      return (
                        <button
                          key={sub.subject_id}
                          onClick={() => onSubjectChange(sub)}
                          className={`w-full text-left p-4 rounded-2xl border transition-all duration-300 relative z-10 flex items-start gap-4 cursor-pointer ${
                            isSelected 
                              ? 'bg-theme-surface border-theme-accent shadow-lg scale-[1.02]' 
                              : 'border-theme-border/40 bg-theme-surface/20 hover:bg-theme-surface/50'
                          }`}
                        >
                          <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 font-mono font-bold text-xs ${
                            isSelected ? 'bg-theme-accent text-white' : 'bg-theme-border text-theme-subtle'
                          }`}>
                            0{idx + 1}
                          </div>
                          
                          <div className="flex-1 space-y-1">
                            <h4 className="font-display font-bold text-sm text-theme-text">
                              {sub.name}
                            </h4>
                            <div className="flex items-center gap-3 text-[10px] font-mono text-theme-subtle">
                              <span className="text-theme-accent font-semibold">{sub.difficulty}</span>
                              <span>•</span>
                              <span>{sub.metadata?.estimated_hours || 40} Hours</span>
                            </div>
                          </div>
                          <ChevronRight size={14} className={`text-theme-subtle self-center transition-transform ${isSelected ? 'translate-x-1 text-theme-accent' : ''}`} />
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Right Side: Modules & Concepts Schema Tree */}
                <div className="lg:col-span-8 bg-theme-surface/30 border border-theme-border rounded-3xl p-6 md:p-8 shadow-xl flex flex-col justify-between relative">
                  
                  {selectedSubject ? (
                    <div className="space-y-6">
                      
                      {/* Subject Metadata Card Header */}
                      <div className="border-b border-theme-border/50 pb-6">
                        <div className="flex flex-wrap justify-between items-center gap-3">
                          <div>
                            <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/10 border border-theme-accent/20 px-2.5 py-0.5 rounded-md">
                              {selectedSubject.subject_id.replace("-", " ")}
                            </span>
                            <h3 className="font-display font-extrabold text-xl text-theme-text mt-2">
                              {selectedSubject.name} Curriculum Map
                            </h3>
                          </div>
                          <div className="flex items-center gap-4 text-xs font-mono text-theme-subtle">
                            <div className="flex items-center gap-1">
                              <Layers size={12} className="text-theme-accent" />
                              <span>{selectedSubject.modules?.length || 0} Modules</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock size={12} />
                              <span>{selectedSubject.metadata?.estimated_hours || 40} hrs</span>
                            </div>
                          </div>
                        </div>
                        <p className="text-xs text-theme-subtle leading-relaxed mt-3">
                          {selectedSubject.metadata?.description || "Master these micro-syllabi structures. Step through conceptual derivations and local terminal code tracers."}
                        </p>
                      </div>

                      {/* Tree Flow: Modules & Concepts */}
                      <div className="space-y-6 relative pl-3 border-l border-theme-border/40">
                        {selectedSubject.modules?.map((mod, idx) => (
                          <div key={mod.id} className="relative space-y-3 group">
                            {/* Connector dot */}
                            <div className="absolute -left-[16.5px] top-1.5 w-2 h-2 rounded-full bg-theme-border group-hover:bg-theme-accent transition-colors" />

                            <div className="space-y-1">
                              <div className="flex items-center gap-2">
                                <span className="text-[10px] font-mono text-theme-accent font-semibold">Module {idx + 1}</span>
                                <span className="text-[10px] text-theme-subtle font-mono">({mod.duration || '45m'})</span>
                              </div>
                              <h5 className="font-display font-bold text-sm text-theme-text">
                                {mod.title}
                              </h5>
                              <p className="text-xs text-theme-subtle leading-relaxed">
                                {mod.description}
                              </p>
                            </div>

                            {/* Conceptual Nodes Checklist */}
                            <div className="flex flex-wrap gap-2 pt-1.5">
                              {mod.topics?.map(topic => (
                                <Link 
                                  key={topic}
                                  to={`/learn/${mod.id}`}
                                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-theme-bg/40 border border-theme-border hover:border-theme-accent/50 text-[11px] font-semibold text-theme-text hover:text-theme-accent transition-all hover:scale-[1.01]"
                                >
                                  <GitCommit size={10} className="text-theme-accent" />
                                  <span>{topic}</span>
                                </Link>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>

                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center py-20 text-center space-y-4">
                      <HelpCircle className="text-theme-subtle/30 animate-pulse-soft" size={40} />
                      <h4 className="font-display font-bold text-sm text-theme-text">No subject selected</h4>
                      <p className="text-xs text-theme-subtle max-w-xs leading-relaxed">
                        Choose a subject node from the timeline sidebar to expand its modules mapping tree.
                      </p>
                    </div>
                  )}

                  {/* Start learning pathway action button */}
                  {selectedSubject && (
                    <div className="mt-8 pt-6 border-t border-theme-border/50 flex justify-end">
                      <Link
                        to={`/learn/${selectedSubject.modules?.[0]?.id || 'ml-foundations'}`}
                        className="bg-theme-accent hover:opacity-90 hover:scale-[1.02] hover:shadow-lg hover:shadow-theme-accent/15 text-white font-bold px-6 py-3 rounded-xl transition-all shadow-md active:scale-[0.98] duration-200 flex items-center gap-2 cursor-pointer text-xs"
                      >
                        <Play size={12} fill="white" />
                        <span>Launch Study Pathway</span>
                      </Link>
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
