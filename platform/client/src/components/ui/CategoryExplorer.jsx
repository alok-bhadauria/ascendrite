import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Play, Compass, GitCommit } from 'lucide-react';

// ==============================================================================
// Subject-specific curiosity-driven process visualizers
// ==============================================================================
function SubjectPreviewVisualizer({ subjectId }) {
  const normalizedId = subjectId?.toLowerCase() || '';

  // 1. Machine Learning / Deep Learning / NLP
  if (normalizedId.includes('machine-learning') || normalizedId.includes('deep-learning') || normalizedId.includes('nlp') || normalizedId.includes('genai') || normalizedId.includes('ai-agents')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// neural_forward_prop</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">Activation Propagation Flow</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Traces how vectors feed forward through weight matrices. Input cells map signals to hidden nodes, firing non-linear threshold values.
          </p>
        </div>
        
        {/* Animated Network SVG */}
        <div className="flex-1 flex items-center justify-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40">
          <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
            {/* Connection Lines with flow animations */}
            <line x1="20" y1="20" x2="100" y2="20" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="20" x2="100" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="50" x2="100" y2="20" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="50" x2="100" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="50" x2="100" y2="80" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="80" x2="100" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="20" y1="80" x2="100" y2="80" stroke="var(--color-theme-border)" strokeWidth="1" />
            
            <line x1="100" y1="20" x2="180" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="100" y1="50" x2="180" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="100" y1="80" x2="180" y2="50" stroke="var(--color-theme-border)" strokeWidth="1" />

            {/* Active pulsing lines */}
            <line x1="20" y1="20" x2="100" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
            <line x1="20" y1="50" x2="100" y2="20" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
            <line x1="100" y1="20" x2="180" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
            <line x1="100" y1="80" x2="180" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />

            {/* Nodes */}
            <circle cx="20" cy="20" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <circle cx="20" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <circle cx="20" cy="80" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            
            <circle cx="100" cy="20" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-pulse" />
            <circle cx="100" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <circle cx="100" cy="80" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-pulse" />
            
            <circle cx="180" cy="50" r="6" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
          </svg>
          <div className="absolute bottom-1 right-2 text-[8px] font-mono text-theme-subtle">Loss: 0.042</div>
        </div>
      </div>
    );
  }

  // 2. Operating Systems
  if (normalizedId.includes('os') || normalizedId.includes('operating-systems') || normalizedId.includes('thread')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// cpu_context_switch</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">CPU Scheduler Switcher</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Traces context switching intervals. CPU registers push and pop active execution stacks between kernel and user modes.
          </p>
        </div>

        {/* Dynamic Gantt queue */}
        <div className="flex-1 flex flex-col justify-center p-3 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40 space-y-3">
          <div className="flex items-center space-x-2 text-[9px] font-mono">
            <span className="text-theme-subtle">Core 0:</span>
            <div className="flex-1 h-6 bg-theme-surface border border-theme-border rounded overflow-hidden relative flex items-center">
              <div className="absolute left-0 top-0 bottom-0 w-24 bg-theme-accent/25 border-r border-theme-accent flex items-center justify-center font-bold text-[8px] text-theme-accent animate-pulse-soft">
                Thread_A (Running)
              </div>
              <div className="absolute left-24 top-0 bottom-0 w-16 bg-theme-border/40 border-r border-theme-border flex items-center justify-center font-bold text-[8px] text-theme-subtle">
                Idle
              </div>
              <div className="absolute left-40 top-0 bottom-0 w-28 bg-emerald-500/20 border-r border-emerald-500 flex items-center justify-center font-bold text-[8px] text-emerald-500">
                Thread_B (Ready)
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2 text-[9px] font-mono select-none">
            <span className="text-theme-subtle">Queue:</span>
            <div className="flex-1 flex gap-1.5 overflow-hidden">
              <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px]">T_C</span>
              <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px]">T_D</span>
              <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px] opacity-60">T_E</span>
            </div>
          </div>
          <div className="text-[8px] font-mono text-theme-accent select-none block">
            &gt; syscall_yield() -&gt; switched context in 0.04μs
          </div>
        </div>
      </div>
    );
  }

  // 3. DBMS / SQL
  if (normalizedId.includes('dbms') || normalizedId.includes('sql') || normalizedId.includes('database')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// b_tree_index_traverse</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">B-Tree Search Index</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Visualizes search path traverses inside an index page root. Node pointers comparison routes lookups to appropriate leaf nodes.
          </p>
        </div>

        {/* Search path visualization */}
        <div className="flex-1 flex items-center justify-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40">
          <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
            <line x1="100" y1="15" x2="60" y2="45" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="100" y1="15" x2="140" y2="45" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="60" y1="45" x2="40" y2="75" stroke="var(--color-theme-border)" strokeWidth="1" />
            <line x1="60" y1="45" x2="80" y2="75" stroke="var(--color-theme-border)" strokeWidth="1" />

            <line x1="100" y1="15" x2="60" y2="45" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
            <line x1="60" y1="45" x2="80" y2="75" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />

            <rect x="80" y="8" width="40" height="14" rx="3" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1" />
            <text x="100" y="18" fill="var(--color-theme-text)" fontSize="7" fontWeight="bold" textAnchor="middle">[ 30 | 70 ]</text>
            
            <rect x="42" y="38" width="36" height="14" rx="3" fill="var(--color-theme-surface)" stroke="var(--color-theme-accent)" strokeWidth="1" className="animate-signal-pulse" />
            <text x="60" y="48" fill="var(--color-theme-text)" fontSize="7" fontWeight="bold" textAnchor="middle">[ 10 | 25 ]</text>
            <rect x="122" y="38" width="36" height="14" rx="3" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1" />
            <text x="140" y="48" fill="var(--color-theme-subtle)" fontSize="7" textAnchor="middle">[ 80 | 95 ]</text>

            <circle cx="40" cy="75" r="4.5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1" />
            <circle cx="80" cy="75" r="4.5" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1" />
          </svg>
          <div className="absolute bottom-1 right-2 text-[8px] font-mono text-theme-accent">Query: Key = 28</div>
        </div>
      </div>
    );
  }

  // 4. Computer Networks
  if (normalizedId.includes('cn') || normalizedId.includes('networking') || normalizedId.includes('socket')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// tcp_socket_handshake</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">TCP Socket Handshake</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Traces network layer socket messages negotiation. Packet buffers sync SYN, SYN-ACK, and ACK session flags.
          </p>
        </div>

        {/* Handshake timeline */}
        <div className="flex-1 flex flex-col justify-between p-3 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40 font-mono text-[9px]">
          <div className="flex justify-between text-theme-subtle">
            <span>Client</span>
            <span>Server</span>
          </div>

          <div className="relative h-16 border-x border-theme-border/60">
            <div className="absolute top-2 w-[80%] h-0.5 bg-dashed border-t border-theme-accent/60 animate-packet" />
            <div className="absolute top-8 right-2 w-[80%] h-0.5 bg-dashed border-t border-emerald-500/60" style={{ transform: 'rotate(180deg)' }} />
            
            <div className="absolute top-1 left-2 text-[8px] text-theme-accent">SYN ➔</div>
            <div className="absolute top-7 right-2 text-[8px] text-emerald-500">&lt; SYN-ACK</div>
          </div>

          <div className="flex justify-between items-center text-[8px]">
            <span className="text-theme-subtle">Status:</span>
            <span className="text-theme-accent font-bold">ESTABLISHED</span>
          </div>
        </div>
      </div>
    );
  }

  // 5. DSA / Algorithms
  if (normalizedId.includes('dsa') || normalizedId.includes('tree') || normalizedId.includes('algorithm') || normalizedId.includes('oop')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// tree_node_traverse</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">Binary Node Traversal</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Visualizes dynamic depth recursion algorithms. Tree nodes comparison pathways are color highlights dynamically.
          </p>
        </div>

        {/* Tree Traverse animated */}
        <div className="flex-1 flex items-center justify-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40">
          <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
            <line x1="100" y1="20" x2="60" y2="50" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <line x1="100" y1="20" x2="140" y2="50" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <line x1="60" y1="50" x2="40" y2="80" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <line x1="60" y1="50" x2="80" y2="80" stroke="var(--color-theme-border)" strokeWidth="1.5" />

            <circle cx="100" cy="20" r="6" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
            <circle cx="60" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" className="animate-node-seq" />
            <circle cx="140" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <circle cx="40" cy="80" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <circle cx="80" cy="80" r="5" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
          </svg>
          <div className="absolute bottom-1 right-2 text-[8px] font-mono text-theme-subtle">DFS Traversal</div>
        </div>
      </div>
    );
  }

  // 6. Web Development / Javascript / ReactJS
  if (normalizedId.includes('react') || normalizedId.includes('next') || normalizedId.includes('javascript') || normalizedId.includes('typescript') || normalizedId.includes('framework')) {
    return (
      <div className="flex flex-col h-full justify-between space-y-4">
        <div>
          <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// virtual_dom_reconcile</span>
          <h5 className="font-display font-bold text-xs text-theme-text mt-1">Virtual DOM Diff Ticks</h5>
          <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
            Traces component tree state updates. Reconciler matches changes in virtual nodes to repaint delta layout sectors.
          </p>
        </div>

        <div className="flex-1 flex justify-around items-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40 text-[8px] font-mono">
          <div className="flex flex-col items-center space-y-1.5">
            <span className="text-theme-accent">Virtual DOM</span>
            <div className="w-12 h-12 border border-theme-border rounded flex flex-col justify-around p-1 bg-theme-surface">
              <div className="w-full h-2 bg-theme-accent/20 rounded animate-pulse" />
              <div className="w-8 h-2 bg-theme-border rounded" />
            </div>
          </div>
          
          <div className="h-0.5 w-8 bg-dashed border-t border-theme-border" />

          <div className="flex flex-col items-center space-y-1.5">
            <span className="text-emerald-500">Real DOM</span>
            <div className="w-12 h-12 border border-theme-border rounded flex flex-col justify-around p-1 bg-theme-surface">
              <div className="w-full h-2 bg-emerald-500/20 rounded" />
              <div className="w-8 h-2 bg-theme-border rounded" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 7. Default concentric orbits
  return (
    <div className="flex flex-col h-full justify-between space-y-4">
      <div>
        <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">// active_domain_taxonomy</span>
        <h5 className="font-display font-bold text-xs text-theme-text mt-1">Curriculum Core Taxonomy</h5>
        <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
          Illustrates core concepts dependency tree mapping categories, subjects, and study progress logs.
        </p>
      </div>

      <div className="flex-1 flex items-center justify-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40">
        <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
          <circle cx="100" cy="50" r="36" fill="none" stroke="var(--color-theme-border)" strokeWidth="0.75" strokeDasharray="3" />
          <circle cx="100" cy="50" r="22" fill="none" stroke="var(--color-theme-border)" strokeWidth="0.75" />
          <circle cx="100" cy="50" r="8" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
          
          <circle cx="122" cy="35" r="3" fill="var(--color-theme-accent)" className="animate-signal-pulse" />
          <circle cx="64" cy="50" r="3" fill="var(--color-theme-border)" />
        </svg>
      </div>
    </div>
  );
}

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
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start max-w-7xl mx-auto">
            
            {/* 1. Left Nav: Category Selection Sidebar (Domain level) */}
            <div className="lg:col-span-3 flex flex-col gap-2 w-full">
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
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-6 sm:p-8 shadow-xl grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch min-h-[440px] animate-fade-in w-full">
                
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
              <div className="lg:col-span-9 bg-theme-surface border border-theme-border rounded-3xl p-6 sm:p-8 shadow-xl grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch min-h-[460px] animate-fade-in w-full">
                
                {/* 2.1 Timeline of Subjects under Category (Left panel inside Card) */}
                <div className="md:col-span-4 flex flex-col justify-between border-b md:border-b-0 md:border-r border-theme-border/60 pb-6 md:pb-0 md:pr-6">
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
                <div className="md:col-span-8 grid grid-cols-1 xl:grid-cols-2 gap-8 items-stretch">
                  {selectedSubject ? (
                    <>
                      {/* Left: Scrollable Modules Timeline */}
                      <div className="flex flex-col justify-between space-y-4">
                        <div>
                          <div className="flex justify-between items-center pb-3 border-b border-theme-border/50 mb-4">
                            <span className="text-[10px] font-mono font-bold text-theme-subtle uppercase tracking-wider">
                              Syllabus Nodes
                            </span>
                            <span className="text-[10px] font-mono text-theme-accent">
                              {selectedSubject.modules?.length || 0} Modules
                            </span>
                          </div>

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

                                <div className="flex flex-wrap gap-1.5 pt-1">
                                  {mod.topics?.map(topic => {
                                    const isObj = typeof topic === 'object' && topic !== null;
                                    const topicKey = isObj ? (topic.id || topic.title) : topic;
                                    const topicLabel = isObj ? (topic.title || topic.id) : topic;
                                    const topicLink = isObj ? `/learn/${topic.id || mod.id}` : `/learn/${mod.id}`;
                                    return (
                                      <Link
                                        key={topicKey}
                                        to={topicLink}
                                        className="flex items-center gap-1 px-2 py-0.5 rounded bg-theme-bg/60 border border-theme-border hover:border-theme-accent/50 text-[9px] text-theme-text hover:text-theme-accent transition-colors"
                                      >
                                        <GitCommit size={8} className="text-theme-accent" />
                                        <span>{topicLabel}</span>
                                      </Link>
                                    );
                                  })}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="text-[9px] font-mono text-theme-subtle text-right border-t border-theme-border/30 pt-3">
                          Path: {selectedSubject.subject_id} &gt; active_modules
                        </div>
                      </div>

                      {/* Right: Technical Curiosity Preview Visualizer */}
                      <div className="flex flex-col justify-between bg-theme-bg/30 border border-theme-border/50 rounded-2xl p-4.5 min-h-[280px]">
                        <SubjectPreviewVisualizer subjectId={selectedSubject.subject_id} />
                      </div>
                    </>
                  ) : (
                    <div className="xl:col-span-2 flex flex-col items-center justify-center h-full text-center p-4">
                      <Compass size={24} className="text-theme-subtle/40 animate-spin-slow" />
                      <p className="text-xs text-theme-subtle font-mono mt-2">Select a subject pathway node</p>
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
