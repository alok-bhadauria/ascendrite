import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Play, Compass } from 'lucide-react';

// ==============================================================================
// 1. EXTENSIBLE VISUALIZER REGISTRY SCHEMA CONFIG
// ==============================================================================
const VISUALIZER_REGISTRY = {
  'machine-learning': {
    tag: '// neural_forward_prop',
    title: 'Activation Propagation Flow',
    desc: 'Traces how vectors feed forward through weight matrices. Input cells map signals to hidden nodes, firing non-linear threshold values.',
    renderType: 'neural-net'
  },
  'deep-learning': {
    tag: '// layer_backpropagation',
    title: 'Gradient Descent Curvatures',
    desc: 'Traces error gradient vectors backward. Weight parameters shift iteratively to minimize loss matrices.',
    renderType: 'neural-net'
  },
  'nlp': {
    tag: '// attention_head_weights',
    title: 'Self-Attention Scalar Products',
    desc: 'Visualizes vector token weights correlation. Query and Key vectors multiply to map contextual word distributions.',
    renderType: 'neural-net'
  },
  'genai': {
    tag: '// latent_diffusion_step',
    title: 'Diffusion Noise Removal',
    desc: 'Traces statistical noise prediction steps. Latent variables filter iteratively to resolve high-fidelity output features.',
    renderType: 'neural-net'
  },
  'ai-agents': {
    tag: '// tool_execution_loop',
    title: 'State Action Planner Ticks',
    desc: 'Traces agent execution loops. Actions check environment observations to invoke tool pipelines dynamically.',
    renderType: 'neural-net'
  },
  'os': {
    tag: '// cpu_context_switch',
    title: 'CPU Thread Scheduler',
    desc: 'Traces context switching intervals. CPU registers push and pop active execution stacks between ready threads.',
    renderType: 'cpu-gantt'
  },
  'operating-systems': {
    tag: '// cpu_context_switch',
    title: 'CPU Thread Scheduler',
    desc: 'Traces context switching intervals. CPU registers push and pop active execution stacks between ready threads.',
    renderType: 'cpu-gantt'
  },
  'dbms': {
    tag: '// b_tree_index_traverse',
    title: 'B-Tree Search Index',
    desc: 'Visualizes search path traverses inside an index page root. Node pointers comparison routes lookups to appropriate leaf nodes.',
    renderType: 'btree-search'
  },
  'sql': {
    tag: '// query_planner_execution',
    title: 'SQL Relational Plan Hash Join',
    desc: 'Traces relational join sequences. Select scans probe hash tables to match row keys dynamically.',
    renderType: 'btree-search'
  },
  'cn': {
    tag: '// tcp_socket_handshake',
    title: 'TCP Socket Handshake',
    desc: 'Traces network layer socket messages negotiation. Packet buffers sync SYN, SYN-ACK, and ACK session flags.',
    renderType: 'socket-handshake'
  },
  'dsa': {
    tag: '// tree_node_traverse',
    title: 'Binary Node Traversal',
    desc: 'Visualizes dynamic depth recursion algorithms. Tree nodes comparison pathways are color highlights dynamically.',
    renderType: 'tree-traverse'
  },
  'oop': {
    tag: '// class_inheritance_dependency',
    title: 'Polymorphic Method Dispatch',
    desc: 'Traces method resolution tables (vtables) lookup. Class methods resolve parent overrides dynamically at runtime.',
    renderType: 'tree-traverse'
  },
  'java': {
    tag: '// JVM_bytecode_execution',
    title: 'JVM Stack Frame Allocation',
    desc: 'Traces Java bytecodes executing on the heap. Method calls push active registers and local variable tables.',
    renderType: 'tree-traverse'
  },
  'spring-boot': {
    tag: '// dependency_injection_beans',
    title: 'ApplicationContext Registry',
    desc: 'Traces inversion-of-control (IoC) initialization. Spring instantiates and injects scoped singleton beans.',
    renderType: 'tree-traverse'
  },
  'system-design': {
    tag: '// load_balancer_distribution',
    title: 'Consistent Hashing Ring',
    desc: 'Traces server nodes hash key ring distribution. Request packets route to appropriate cache nodes seamlessly.',
    renderType: 'hashing-ring'
  },
  'reactjs': {
    tag: '// virtual_dom_reconcile',
    title: 'Virtual DOM Diff Ticks',
    desc: 'Traces component tree state updates. Reconciler matches changes in virtual nodes to repaint delta layout sectors.',
    renderType: 'dom-diff'
  },
  'nextjs': {
    tag: '// server_side_reconciliation',
    title: 'Hydration Pipeline Ticks',
    desc: 'Traces server-rendered nodes hydration. Browser binds event listeners dynamically onto static DOM nodes.',
    renderType: 'dom-diff'
  },
  'html-css-git': {
    tag: '// browser_layout_engine',
    title: 'Layout Engine Paint Tree',
    desc: 'Traces browser layout rendering. DOM tree nodes merge with CSSOM rules to compute positions and repaint paint arrays.',
    renderType: 'render-pipeline'
  },
  'css-frameworks': {
    tag: '// tailwind_utility_compile',
    title: 'Utility-First Styles Generation',
    desc: 'Traces CSS utility maps compile. Ingested class strings compile to static style rules.',
    renderType: 'render-pipeline'
  },
  'javascript': {
    tag: '// v8_jit_compile',
    title: 'V8 Execution Call Stack',
    desc: 'Traces execution contexts. Functions push and pop scope references on the global V8 event stack.',
    renderType: 'git-flow'
  },
  'typescript': {
    tag: '// static_type_checker',
    title: 'TS AST Type Assertion Ticks',
    desc: 'Traces compilation type assertions. Compiler scans parameter bindings to raise lint errors before runtime.',
    renderType: 'git-flow'
  },
  'nodejs-expressjs': {
    tag: '// express_middleware_chain',
    title: 'Middleware Execution Pipe',
    desc: 'Traces route interceptor pipelines. Request vectors trigger sequential handler callbacks.',
    renderType: 'git-flow'
  }
};

// ==============================================================================
// 2. MODULAR RENDERERS FOR SYSTEM PREVIEWS
// ==============================================================================
function RenderNeuralNet() {
  return (
    <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
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
      
      <line x1="20" y1="20" x2="100" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
      <line x1="20" y1="50" x2="100" y2="20" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
      <line x1="100" y1="20" x2="180" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
      <line x1="100" y1="80" x2="180" y2="50" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />

      <circle cx="20" cy="20" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="20" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="20" cy="80" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="100" cy="20" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-pulse" />
      <circle cx="100" cy="50" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="100" cy="80" r="5" fill="var(--color-theme-surface)" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-pulse" />
      <circle cx="180" cy="50" r="6" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
    </svg>
  );
}

function RenderCpuGantt() {
  return (
    <div className="flex flex-col justify-center space-y-3 h-28 font-mono text-[9px]">
      <div className="flex items-center space-x-2">
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
      <div className="flex items-center space-x-2 select-none">
        <span className="text-theme-subtle">Queue:</span>
        <div className="flex-1 flex gap-1.5 overflow-hidden">
          <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px]">T_C</span>
          <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px]">T_D</span>
          <span className="px-1.5 py-0.5 rounded bg-theme-surface border border-theme-border text-[8px] opacity-60">T_E</span>
        </div>
      </div>
    </div>
  );
}

function RenderBTree() {
  return (
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
  );
}

function RenderSocket() {
  return (
    <div className="h-28 flex flex-col justify-between font-mono text-[9px]">
      <div className="flex justify-between text-theme-subtle">
        <span>Client</span>
        <span>Server</span>
      </div>
      <div className="relative h-12 border-x border-theme-border/60">
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
  );
}

function RenderTree() {
  return (
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
  );
}

function RenderDomDiff() {
  return (
    <div className="flex justify-around items-center h-28 text-[8px] font-mono w-full">
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
  );
}

function RenderHashingRing() {
  return (
    <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
      <circle cx="100" cy="50" r="32" fill="none" stroke="var(--color-theme-border)" strokeWidth="1" strokeDasharray="3" />
      <circle cx="100" cy="50" r="6" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1" />
      <circle cx="100" cy="18" r="4" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="132" cy="50" r="4" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="68" cy="50" r="4" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <path d="M 100 50 L 132 50" stroke="var(--color-theme-accent)" strokeWidth="1" className="animate-signal-flow" />
      <text x="100" y="10" fill="var(--color-theme-text)" fontSize="6" textAnchor="middle">Node_A</text>
      <text x="146" y="52" fill="var(--color-theme-text)" fontSize="6" textAnchor="middle">Node_B</text>
    </svg>
  );
}

function RenderPipeline() {
  return (
    <div className="flex justify-around items-center h-28 text-[9px] font-mono w-full select-none">
      <div className="px-2 py-1 bg-theme-surface border border-theme-border rounded">DOM</div>
      <span className="text-theme-subtle">➔</span>
      <div className="px-2 py-1 bg-theme-surface border border-theme-border rounded">CSSOM</div>
      <span className="text-theme-subtle">➔</span>
      <div className="px-2 py-1 bg-theme-accent/10 border border-theme-accent text-theme-accent rounded animate-pulse">Layout</div>
      <span className="text-theme-subtle">➔</span>
      <div className="px-2 py-1 bg-theme-surface border border-theme-border rounded">Paint</div>
    </div>
  );
}

function RenderGitFlow() {
  return (
    <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
      <line x1="20" y1="30" x2="180" y2="30" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <path d="M 50 30 Q 80 70 120 70 Q 150 30 180 30" fill="none" stroke="var(--color-theme-border)" strokeWidth="1.5" strokeDasharray="3" />
      <line x1="80" y1="30" x2="120" y2="70" stroke="var(--color-theme-accent)" strokeWidth="1.5" className="animate-signal-flow" />
      <circle cx="40" cy="30" r="4.5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="80" cy="30" r="4.5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
      <circle cx="100" cy="70" r="4" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
      <circle cx="150" cy="30" r="4.5" fill="var(--color-theme-surface)" stroke="var(--color-theme-border)" strokeWidth="1.5" />
    </svg>
  );
}

function RenderDefault() {
  return (
    <svg className="w-full h-full max-h-[140px]" viewBox="0 0 200 100">
      <circle cx="100" cy="50" r="36" fill="none" stroke="var(--color-theme-border)" strokeWidth="0.75" strokeDasharray="3" />
      <circle cx="100" cy="50" r="22" fill="none" stroke="var(--color-theme-border)" strokeWidth="0.75" />
      <circle cx="100" cy="50" r="8" fill="var(--color-theme-accent)" stroke="var(--color-theme-bg)" strokeWidth="1.5" />
      <circle cx="122" cy="35" r="3" fill="var(--color-theme-accent)" className="animate-signal-pulse" />
      <circle cx="64" cy="50" r="3" fill="var(--color-theme-border)" />
    </svg>
  );
}

// ==============================================================================
// 3. EXTENSIBLE RENDERER COMPONENT
// ==============================================================================
function SubjectPreviewVisualizer({ subjectId }) {
  const normId = subjectId?.toLowerCase() || '';
  
  // Lookup configuration dynamically from registry
  const visualMeta = VISUALIZER_REGISTRY[normId] || {
    tag: '// active_domain_taxonomy',
    title: 'Curriculum Core Taxonomy',
    desc: 'Illustrates core concepts dependency tree mapping categories, subjects, and study progress logs.',
    renderType: 'default'
  };

  const renderVisualizerContent = () => {
    switch (visualMeta.renderType) {
      case 'neural-net':        return <RenderNeuralNet />;
      case 'cpu-gantt':         return <RenderCpuGantt />;
      case 'btree-search':      return <RenderBTree />;
      case 'socket-handshake':  return <RenderSocket />;
      case 'tree-traverse':     return <RenderTree />;
      case 'dom-diff':          return <RenderDomDiff />;
      case 'hashing-ring':      return <RenderHashingRing />;
      case 'render-pipeline':   return <RenderPipeline />;
      case 'git-flow':          return <RenderGitFlow />;
      default:                  return <RenderDefault />;
    }
  };

  return (
    <div className="flex flex-col h-full justify-between space-y-4">
      <div>
        <span className="text-[9px] font-mono text-theme-accent uppercase font-bold tracking-wider">
          {visualMeta.tag}
        </span>
        <h5 className="font-display font-bold text-xs text-theme-text mt-1">
          {visualMeta.title}
        </h5>
        <p className="text-[10px] text-theme-subtle mt-1 leading-normal">
          {visualMeta.desc}
        </p>
      </div>
      
      <div className="flex-1 flex items-center justify-center p-2 bg-theme-bg/50 border border-theme-border/60 rounded-xl relative overflow-hidden h-40">
        {renderVisualizerContent()}
      </div>
    </div>
  );
}

// ==============================================================================
// 4. MAIN CURRICULUM EXPLORER ATLAS
// ==============================================================================
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
                    <text x="44" y="52.5" fill="var(--color-theme-text)" fontSize="7" fontWeight="bold" textAnchor="middle">Root</text>
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
                      {/* Left: Scrollable Modules Timeline Teaser */}
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
                            {selectedSubject.modules?.slice(0, 2).map((mod, idx) => (
                              <div key={mod.id || idx} className="space-y-2 border-l border-theme-border/50 pl-3 relative group">
                                <div className="absolute -left-[4.5px] top-1.5 w-2 h-2 rounded-full bg-theme-border group-hover:bg-theme-accent transition-colors" />
                                
                                <div className="flex items-center gap-2 text-[9px] font-mono">
                                  <span className="text-theme-accent font-semibold">M0{idx + 1}</span>
                                </div>
                                <h6 className="font-display font-bold text-xs text-theme-text leading-snug">
                                  {mod.title || mod.name}
                                </h6>
                                <p className="text-[11px] text-theme-subtle leading-relaxed">
                                  {mod.description}
                                </p>
                              </div>
                            ))}
                            {selectedSubject.modules?.length > 2 && (
                              <div className="border-l border-theme-border/50 pl-3 py-2.5">
                                <div className="bg-theme-accent/5 border border-dashed border-theme-accent/30 rounded-xl p-3.5 select-none text-[10px] font-mono text-theme-subtle leading-relaxed">
                                  <span className="text-theme-accent font-bold block mb-1">✦ Dynamic Pathway Locked</span>
                                  Unlock {selectedSubject.modules.length - 2} additional advanced system modules, structural trace tests, and progress indexes after creating a free account.
                                </div>
                              </div>
                            )}
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
