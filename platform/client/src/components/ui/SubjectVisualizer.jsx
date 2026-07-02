import React from 'react';
import { Code, Cpu } from 'lucide-react';

/**
 * SubjectVisualizer renders a mini interactive preview diagram
 * for the currently selected subject in the curriculum explorer.
 * Each visualizer is a lightweight inline SVG or HTML representation
 * of a core concept from that subject's domain.
 */
export default function SubjectVisualizer({ selectedSubject }) {
  if (!selectedSubject) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-4">
        <div className="w-10 h-10 rounded-xl bg-theme-accent/10 border border-theme-border/40 flex items-center justify-center text-theme-accent animate-spin-slow">
          <Cpu size={18} />
        </div>
        <p className="text-xs text-theme-subtle font-mono mt-3">Select a subject pipeline</p>
      </div>
    );
  }

  const name = selectedSubject.name.toLowerCase();
  const id = selectedSubject.subject_id.toLowerCase();

  // 1. MACHINE LEARNING
  if (id === 'machine-learning' || name.includes('machine learning')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Linear Regression Fit</span>
        <div className="flex-1 relative flex items-center justify-center p-4">
          <svg className="w-full h-40 bg-theme-surface border border-theme-border rounded-2xl" style={{ minHeight: '160px' }}>
            <line x1="10%" y1="85%" x2="90%" y2="15%" stroke="var(--color-theme-accent)" strokeWidth="3" className="animate-pulse" />
            <circle cx="20%" cy="75%" r="7" fill="#10b981" />
            <line x1="20%" y1="75%" x2="20%" y2="76%" stroke="#10b981" strokeWidth="1.5" strokeDasharray="3" />
            <circle cx="40%" cy="55%" r="7" fill="#10b981" />
            <circle cx="50%" cy="65%" r="7" fill="#f43f5e" />
            <line x1="50%" y1="65%" x2="50%" y2="50%" stroke="#f43f5e" strokeWidth="1.5" strokeDasharray="3" />
            <circle cx="70%" cy="30%" r="7" fill="#10b981" />
            <circle cx="80%" cy="28%" r="7" fill="#f43f5e" />
            <line x1="80%" y1="28%" x2="80%" y2="24%" stroke="#f43f5e" strokeWidth="1.5" strokeDasharray="3" />
          </svg>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Regression Gradient Descent: Minimizing MSE Loss</span>
      </div>
    );
  }

  // 2. DEEP LEARNING
  if (id === 'deep-learning' || name.includes('deep learning')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Feed-Forward Neural Net</span>
        <div className="flex-1 relative flex items-center justify-center p-4">
          <svg className="w-full h-40 bg-theme-surface border border-theme-border rounded-2xl" style={{ minHeight: '160px' }}>
            <line x1="20%" y1="25%" x2="50%" y2="25%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="20%" y1="25%" x2="50%" y2="50%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="20%" y1="25%" x2="50%" y2="75%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="20%" y1="75%" x2="50%" y2="25%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="20%" y1="75%" x2="50%" y2="50%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="20%" y1="75%" x2="50%" y2="75%" stroke="var(--color-theme-text)" strokeWidth="2.5" opacity="0.15" />
            <line x1="50%" y1="25%" x2="80%" y2="50%" stroke="var(--color-theme-accent)" strokeWidth="2.5" opacity="0.3" />
            <line x1="50%" y1="50%" x2="80%" y2="50%" stroke="var(--color-theme-accent)" strokeWidth="2.5" opacity="0.3" />
            <line x1="50%" y1="75%" x2="80%" y2="50%" stroke="var(--color-theme-accent)" strokeWidth="2.5" opacity="0.3" />
            <circle r="4.5" fill="var(--color-theme-accent)">
              <animateMotion path="M 20,25 L 50,50 L 80,50" dur="2s" repeatCount="indefinite" />
            </circle>
            <circle r="4.5" fill="#10b981">
              <animateMotion path="M 20,75 L 50,25 L 80,50" dur="2.5s" repeatCount="indefinite" />
            </circle>
            <circle cx="20%" cy="25%" r="10" fill="#10b981" />
            <text x="17%" y="28%" fill="white" fontSize="8" fontWeight="bold">I1</text>
            <circle cx="20%" cy="75%" r="10" fill="#10b981" />
            <text x="17%" y="78%" fill="white" fontSize="8" fontWeight="bold">I2</text>
            <circle cx="50%" cy="25%" r="10" fill="var(--color-theme-accent)" />
            <text x="47%" y="28%" fill="white" fontSize="8" fontWeight="bold">H1</text>
            <circle cx="50%" cy="50%" r="10" fill="var(--color-theme-accent)" />
            <text x="47%" y="53%" fill="white" fontSize="8" fontWeight="bold">H2</text>
            <circle cx="50%" cy="75%" r="10" fill="var(--color-theme-accent)" />
            <text x="47%" y="78%" fill="white" fontSize="8" fontWeight="bold">H3</text>
            <circle cx="80%" cy="50%" r="10" fill="#8b5cf6" />
            <text x="77%" y="53%" fill="white" fontSize="8" fontWeight="bold">Out</text>
          </svg>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Forward propagation of nodes with weights &amp; biases</span>
      </div>
    );
  }

  // 3. AI AGENTS
  if (id === 'ai-agents' || name.includes('agent')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Agent Path Optimization</span>
        <div className="flex-1 flex justify-around items-center p-4">
          <div className="grid grid-cols-4 gap-3 bg-theme-surface border border-theme-border p-4 rounded-2xl shadow-sm">
            <div className="w-9 h-9 bg-theme-accent text-white font-mono text-xs font-bold flex items-center justify-center rounded-lg animate-bounce">A</div>
            <div className="w-9 h-9 bg-theme-border/40 rounded-lg" />
            <div className="w-9 h-9 bg-red-500/20 border border-red-500 rounded-lg flex items-center justify-center font-mono text-[9px] text-red-500 font-bold">Block</div>
            <div className="w-9 h-9 bg-theme-border/40 rounded-lg" />
            <div className="w-9 h-9 bg-theme-accent/20 rounded-lg border-2 border-theme-accent border-dashed animate-pulse" />
            <div className="w-9 h-9 bg-theme-accent/20 rounded-lg border-2 border-theme-accent border-dashed animate-pulse" />
            <div className="w-9 h-9 bg-theme-border/40 rounded-lg" />
            <div className="w-9 h-9 bg-emerald-500 text-white font-mono text-xs font-bold flex items-center justify-center rounded-lg shadow">Goal</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Solving path bounds: A* state heuristics loop</span>
      </div>
    );
  }

  // 4. GENAI
  if (id === 'genai' || name.includes('genai') || name.includes('generative')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">LLM Token Probability Weights</span>
        <div className="flex-1 flex flex-col justify-center items-stretch gap-3 p-4">
          <div className="bg-theme-surface border border-theme-border p-3 rounded-xl font-mono text-xs text-theme-text font-bold shadow-inner">
            Prompt: &quot;Deep Learning is...&quot;
          </div>
          <div className="flex flex-col gap-2 pl-3 border-l-3 border-theme-accent/40">
            <div className="flex justify-between items-center text-xs">
              <span className="font-extrabold text-theme-accent">1. &quot;revolutionary&quot;</span>
              <span className="font-mono bg-theme-border px-2.5 py-0.5 rounded-lg text-theme-text font-bold">p=0.68</span>
            </div>
            <div className="flex justify-between items-center text-xs opacity-70">
              <span>2. &quot;complex&quot;</span>
              <span className="font-mono bg-theme-border px-2.5 py-0.5 rounded-lg font-bold">p=0.22</span>
            </div>
            <div className="flex justify-between items-center text-xs opacity-50">
              <span>3. &quot;expensive&quot;</span>
              <span className="font-mono bg-theme-border px-2.5 py-0.5 rounded-lg font-bold">p=0.10</span>
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Sampling token distributions via Softmax scaling</span>
      </div>
    );
  }

  // 5. NLP
  if (id === 'nlp' || name.includes('nlp') || name.includes('language')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Semantic Embedding Projections</span>
        <div className="flex-1 relative flex items-center justify-center p-4">
          <svg className="w-full h-40 bg-theme-surface border border-theme-border rounded-2xl animate-pulse-soft" style={{ minHeight: '160px' }}>
            <line x1="10%" y1="90%" x2="95%" y2="90%" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <line x1="10%" y1="5%" x2="10%" y2="90%" stroke="var(--color-theme-border)" strokeWidth="1.5" />
            <text x="25%" y="75%" fill="var(--color-theme-text)" fontSize="11" fontWeight="extrabold">King</text>
            <text x="75%" y="25%" fill="var(--color-theme-accent)" fontSize="11" fontWeight="extrabold" className="animate-pulse">Queen</text>
            <text x="20%" y="40%" fill="var(--color-theme-text)" fontSize="11" fontWeight="extrabold">Man</text>
            <text x="65%" y="60%" fill="var(--color-theme-text)" fontSize="11" fontWeight="extrabold">Woman</text>
            <line x1="30%" y1="70%" x2="70%" y2="30%" stroke="var(--color-theme-accent)" strokeWidth="2.5" strokeDasharray="4" />
          </svg>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Vector Cosine: King - Man + Woman = Queen</span>
      </div>
    );
  }

  // 6. DBMS
  if (id === 'dbms' || name.includes('dbms')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Index Seek vs. Full Scan</span>
        <div className="flex-grow flex flex-col sm:flex-row items-center justify-around gap-3 p-4">
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-border p-3 rounded-xl w-32 shadow-sm">
            <span className="font-bold text-red-500 font-mono text-xs">Full Table Scan</span>
            <div className="flex flex-col gap-1 w-full">
              <div className="px-2.5 py-1 bg-theme-border/40 rounded border border-theme-border animate-pulse text-[10px] text-center font-bold">Row 1</div>
              <div className="px-2.5 py-1 bg-theme-border/40 rounded border border-theme-border animate-pulse text-[10px] text-center font-bold">Row 2</div>
              <div className="px-2.5 py-1 bg-theme-border/40 rounded border border-theme-border animate-pulse text-[10px] text-center font-bold">Row 3</div>
            </div>
            <span className="text-[9px] font-mono text-theme-subtle mt-1 font-bold">O(N) search (Slow)</span>
          </div>
          <div className="text-theme-accent font-bold text-lg select-none rotate-90 sm:rotate-0 my-1 sm:my-0">&rarr;</div>
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-accent/30 p-3 rounded-xl w-36 shadow">
            <span className="font-bold text-green-500 font-mono text-xs">Indexed Seek</span>
            <div className="flex flex-col items-center gap-1 w-full">
              <div className="px-2.5 py-1 bg-theme-accent text-white rounded font-bold text-[10px] shadow-sm">Root Node</div>
              <div className="flex gap-2 mt-1">
                <div className="px-1.5 py-0.5 bg-theme-border/60 rounded text-[9px]">Left</div>
                <div className="px-1.5 py-0.5 bg-theme-border/60 rounded text-[9px] border border-theme-accent animate-ping">Leaf (Seek)</div>
              </div>
            </div>
            <span className="text-[9px] font-mono text-theme-subtle mt-1 font-bold">O(log N) seek (Fast)</span>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">B+ Tree indices enable fast logarithmic page seeks</span>
      </div>
    );
  }

  // 7. SQL
  if (id === 'sql' || name.includes('sql')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Query Execution Plan Optimizer</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-2 p-4 font-mono">
          <div className="px-3.5 py-1.5 bg-emerald-500 text-white rounded-lg border border-emerald-600 shadow animate-pulse text-xs font-bold">
            {"[3] FILTER (age > 21)"}
          </div>
          <div className="text-theme-subtle text-xs animate-bounce font-bold">&#9650;</div>
          <div className="px-3.5 py-1.5 bg-theme-accent text-white rounded-lg border border-theme-accent shadow text-xs font-bold">
            {"[2] HASH JOIN (users.id = logs.user_id)"}
          </div>
          <div className="text-theme-subtle text-xs font-bold">&#9650;</div>
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="px-2.5 py-1 bg-theme-surface border border-theme-border rounded text-[10px] font-bold">
              [1a] SCAN users Table
            </div>
            <div className="px-2.5 py-1 bg-theme-surface border border-theme-border rounded text-[10px] font-bold">
              [1b] SEEK logs Index
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Compiling declarative queries into relational nodes</span>
      </div>
    );
  }

  // 8. OS
  if (id === 'os' || name.includes('os') || name.includes('operating')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">CPU Thread Round-Robin Scheduler</span>
        <div className="flex-grow flex flex-col sm:flex-row items-center justify-center gap-6 p-4">
          <div className="flex flex-col gap-1.5 bg-theme-surface border border-theme-border p-3 rounded-xl shadow-sm">
            <span className="text-[9px] font-mono text-theme-subtle font-bold">Ready Queue</span>
            <div className="px-2.5 py-1 bg-theme-border rounded text-xs font-bold animate-pulse">Thread 1</div>
            <div className="px-2.5 py-1 bg-theme-border rounded text-xs font-bold">Thread 2</div>
          </div>
          <div className="text-theme-accent font-bold animate-pulse text-xs">
            <span className="sm:hidden">&#9660; Context Switch</span>
            <span className="hidden sm:inline">-- Context Switch --&gt;</span>
          </div>
          <div className="w-20 h-20 rounded-full border-4 border-theme-accent/60 border-t-theme-accent flex flex-col items-center justify-center animate-spin-slow shadow">
            <span className="text-[9px] font-bold text-theme-text select-none">CPU Core</span>
            <span className="text-[8px] font-mono text-emerald-500 font-extrabold select-none">RUNNING</span>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Distributing timeslices: Preemptive kernel scheduler</span>
      </div>
    );
  }

  // 9. CN
  if (id === 'cn' || name.includes('networking') || name.includes('network') || name.includes('cn')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Dijkstra Shortest Path Routing (RIP)</span>
        <div className="flex-1 relative flex items-center justify-center p-4">
          <svg className="w-full h-40 bg-theme-surface border border-theme-border rounded-2xl" style={{ minHeight: '160px' }}>
            <line x1="20%" y1="50%" x2="50%" y2="20%" stroke="var(--color-theme-border)" strokeWidth="2" opacity="0.4" />
            <line x1="20%" y1="50%" x2="50%" y2="80%" stroke="var(--color-theme-border)" strokeWidth="2" opacity="0.4" />
            <line x1="50%" y1="20%" x2="80%" y2="50%" stroke="var(--color-theme-border)" strokeWidth="2" opacity="0.4" />
            <line x1="50%" y1="80%" x2="80%" y2="50%" stroke="var(--color-theme-border)" strokeWidth="2" opacity="0.4" />
            <line x1="20%" y1="50%" x2="50%" y2="20%" stroke="var(--color-theme-accent)" strokeWidth="3" className="animate-pulse" />
            <line x1="50%" y1="20%" x2="80%" y2="50%" stroke="var(--color-theme-accent)" strokeWidth="3" className="animate-pulse" />
            <circle r="5" fill="var(--color-theme-accent)" className="animate-pulse">
              <animateMotion path="M 22,50 L 50,20 L 78,50" dur="3s" repeatCount="indefinite" />
            </circle>
            <circle cx="20%" cy="50%" r="12" fill="#10b981" className="shadow" />
            <text x="16%" y="54%" fill="white" fontSize="9" fontWeight="bold">Src</text>
            <circle cx="50%" cy="20%" r="12" fill="var(--color-theme-accent)" className="shadow" />
            <text x="47%" y="24%" fill="white" fontSize="9" fontWeight="bold">R1</text>
            <circle cx="50%" cy="80%" r="12" fill="var(--color-theme-text)" opacity="0.4" className="shadow" />
            <text x="47%" y="84%" fill="var(--color-theme-bg)" fontSize="9" fontWeight="bold">R2</text>
            <circle cx="80%" cy="50%" r="12" fill="#8b5cf6" className="shadow" />
            <text x="77%" y="54%" fill="white" fontSize="9" fontWeight="bold">Dst</text>
          </svg>
          <div className="absolute top-6 right-6 bg-theme-bg/85 border border-theme-border/60 backdrop-blur px-3 py-2 rounded-xl text-[8px] font-mono text-theme-text space-y-0.5 shadow-md">
            <div className="text-theme-accent font-bold text-[9px]">ROUTE TABLE (R1)</div>
            <div>Dest: 192.168.2.10</div>
            <div>NextHop: R1 (Cost: 2)</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Transmitting IP frames: Dynamic SPF convergence metric maps</span>
      </div>
    );
  }

  // 10. DSA
  if (id === 'dsa' || name.includes('dsa') || name.includes('data structures') || name.includes('algorithm')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Linked Memory Node Pointer</span>
        <div className="flex-grow flex flex-wrap items-center justify-center gap-2.5 sm:gap-3 p-4">
          <div className="px-4 py-2 bg-theme-surface border border-theme-accent rounded-xl shadow-sm text-xs font-mono font-bold animate-pulse text-theme-accent">
            Node A [Val: 42]
          </div>
          <div className="text-theme-subtle animate-bounce font-bold text-xs">{"-->"}</div>
          <div className="px-4 py-2 bg-theme-surface border border-theme-border rounded-xl shadow-sm text-xs font-mono font-bold text-theme-text">
            Node B [Val: 96]
          </div>
          <div className="text-theme-subtle font-bold text-xs">{"-->"}</div>
          <div className="px-4 py-2 bg-theme-surface border border-theme-border rounded-xl shadow-sm text-xs font-mono font-bold text-theme-subtle">
            Null
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Nodes reference next memory segments via addresses</span>
      </div>
    );
  }

  // 11. JAVA
  if (id === 'java' || name.includes('java')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">JVM Runtime Memory Spaces</span>
        <div className="flex-grow flex flex-col sm:flex-row justify-around items-center gap-3 p-4 font-mono text-xs">
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-border p-3 rounded-xl w-28 shadow-sm">
            <span className="font-bold text-theme-accent">JVM Heap Space</span>
            <div className="px-2 py-1 bg-theme-accent/15 border border-theme-accent rounded text-[9px] animate-pulse font-bold">Object Instances</div>
            <span className="text-[8px] text-theme-subtle mt-1 font-bold">Shared Space</span>
          </div>
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-border p-3 rounded-xl w-28 shadow-sm">
            <span className="font-bold text-emerald-500">Execution Stack</span>
            <div className="px-2 py-1 bg-emerald-500/15 border border-emerald-500 rounded text-[9px] font-bold">Frame 1 [Local]</div>
            <span className="text-[8px] text-theme-subtle mt-1 font-bold">Thread Private</span>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Handling scope bindings inside runtime environments</span>
      </div>
    );
  }

  // 12. OOP - responsive fix: flex-col sm:flex-row for the two class cards
  if (id === 'oop' || name.includes('oop') || name.includes('object')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Polymorphism Inheritance Compiler Trees</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-2 p-4 text-xs font-mono">
          <div className="px-3.5 py-1.5 bg-theme-surface border border-theme-border rounded-xl shadow-sm text-theme-accent font-bold">
            Base class: Animal [speak()]
          </div>
          <div className="text-theme-subtle text-xs font-bold">&#9650;</div>
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="px-3 py-1.5 bg-theme-surface border border-theme-accent rounded-xl text-[10px] font-bold animate-pulse">
              {"Dog overrides [speak() -> \"Bark\"]"}
            </div>
            <div className="px-3 py-1.5 bg-theme-surface border border-theme-border rounded-xl text-[10px] font-bold">
              {"Cat overrides [speak() -> \"Meow\"]"}
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Resolving virtual methods at runtime via VTables</span>
      </div>
    );
  }

  // 13. SPRING BOOT
  if (id === 'spring-boot' || name.includes('spring')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Spring MVC Request Dispatcher</span>
        <div className="flex-1 flex justify-around items-center p-4 text-xs font-mono">
          <div className="flex flex-col items-center gap-2 bg-theme-surface border border-theme-border p-3.5 rounded-2xl shadow-sm">
            <div className="px-2.5 py-1 bg-theme-accent text-white rounded-lg text-[10px] font-bold animate-pulse">@RestController</div>
            <div className="text-theme-subtle font-bold">&#9660;</div>
            <div className="px-2.5 py-1 bg-theme-border rounded-lg text-[10px] font-bold">@Service Bean</div>
            <div className="text-theme-subtle font-bold">&#9660;</div>
            <div className="px-2.5 py-1 bg-theme-border rounded-lg text-[10px] font-bold">@Repository Sync</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Injecting dependency properties via Spring IoC containers</span>
      </div>
    );
  }

  // 14. SYSTEM DESIGN - responsive fix: flex-wrap
  if (id === 'system-design' || name.includes('system design')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Load Balancing Cluster Syncing</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-4 p-4">
          <div className="px-4 py-2 bg-theme-accent text-white rounded-xl font-mono text-xs font-bold shadow-md animate-pulse">
            REPLICA LOAD BALANCER
          </div>
          <div className="flex flex-wrap gap-4 sm:gap-8 justify-center">
            <div className="flex flex-col items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-full bg-green-500 animate-ping" />
              <span className="text-xs font-mono text-theme-text font-bold">Node Replica 1</span>
            </div>
            <div className="flex flex-col items-center gap-1.5">
              <span className="w-3.5 h-3.5 rounded-full bg-green-500" />
              <span className="text-xs font-mono text-theme-text font-bold">Node Replica 2</span>
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Distributing client requests across container replicas</span>
      </div>
    );
  }

  // 15. REACTJS - responsive fix: flex-wrap
  if (id === 'reactjs' || name.includes('react')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Virtual DOM Reconciliation</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-4 p-4">
          <div className="flex flex-wrap gap-4 sm:gap-8 relative select-none justify-center items-center">
            <div className="flex flex-col items-center gap-2">
              <span className="text-[10px] font-bold text-theme-subtle uppercase">Previous VDOM</span>
              <div className="w-8 h-8 rounded-full bg-theme-subtle flex items-center justify-center text-white text-[10px] font-bold">Div</div>
            </div>
            <div className="text-theme-accent self-center animate-pulse font-bold text-xs">{"-- Diff -->"}</div>
            <div className="flex flex-col items-center gap-2">
              <span className="text-[10px] font-bold text-theme-accent uppercase animate-pulse">Reconciled DOM</span>
              <div className="w-8 h-8 rounded-full bg-theme-accent flex items-center justify-center text-white text-[10px] font-bold animate-bounce">Div</div>
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Updating specifically modified nodes to prevent page reflows</span>
      </div>
    );
  }

  // 16. JAVASCRIPT
  if (id === 'javascript' || name.includes('javascript') || id === 'js') {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">JS Runtime Event Loop</span>
        <div className="flex-grow flex flex-col sm:flex-row items-center justify-around gap-3 p-4 text-xs font-mono">
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-border p-2.5 rounded-xl w-24 shadow-sm">
            <span className="font-bold text-theme-accent">Call Stack</span>
            <div className="px-2 py-0.5 bg-theme-accent/25 rounded text-[10px] animate-pulse">fetchData()</div>
          </div>
          <div className="w-12 h-12 rounded-full border-4 border-dashed border-theme-accent animate-spin flex items-center justify-center text-[10px] text-theme-accent font-bold">
            Loop
          </div>
          <div className="flex flex-col items-center gap-1.5 bg-theme-surface border border-theme-border p-2.5 rounded-xl w-24 shadow-sm">
            <span className="font-bold text-emerald-500">Task Queue</span>
            <div className="px-2 py-0.5 bg-emerald-500/25 rounded text-[10px]">cbPromise()</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Handling asynchronous tasks via non-blocking worker pools</span>
      </div>
    );
  }

  // 17. TYPESCRIPT - responsive fix: flex-wrap
  if (id === 'typescript' || name.includes('typescript') || id === 'ts') {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Static Compile-Time Type Check</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-2.5 p-4 text-xs font-mono">
          <div className="bg-theme-surface border border-theme-border p-2.5 rounded-xl w-full text-center font-bold">
            <code>function add(a: number, b: number)</code>
          </div>
          <div className="flex flex-wrap gap-2 justify-center">
            <div className="px-2 py-1 bg-red-500/10 border border-red-500 text-red-500 rounded-lg text-[10px] font-bold">
              {"add(\"5\", 10) -> error"}
            </div>
            <div className="px-2 py-1 bg-green-500/10 border border-green-500 text-green-500 rounded-lg text-[10px] font-bold animate-pulse">
              {"add(5, 10) -> OK"}
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Verifying interface structural shapes at compilation phase</span>
      </div>
    );
  }

  // 18. NODEJS & EXPRESSJS - responsive fix: flex-wrap
  if (id === 'nodejs-expressjs' || name.includes('node') || name.includes('express')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Middleware Routing Execution Pipeline</span>
        <div className="flex-1 flex justify-around items-center p-4 text-xs font-mono">
          <div className="flex flex-wrap gap-2 items-center bg-theme-surface border border-theme-border p-3.5 rounded-2xl shadow-sm justify-center">
            <div className="px-2 py-0.5 bg-theme-accent/20 border border-theme-accent text-theme-text rounded font-bold text-[10px]">Request</div>
            <span className="text-theme-subtle font-bold">&rarr;</span>
            <div className="px-2 py-0.5 bg-emerald-500/20 border border-emerald-500 text-emerald-500 rounded animate-pulse font-bold text-[10px]">Auth Check</div>
            <span className="text-theme-subtle font-bold">&rarr;</span>
            <div className="px-2 py-0.5 bg-theme-border rounded font-bold text-[10px]">JSON Parser</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Intercepting response handlers sequentially</span>
      </div>
    );
  }

  // 19. NEXTJS
  if (id === 'nextjs' || name.includes('next')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Server Rendering vs. Hydration</span>
        <div className="flex-grow flex flex-col sm:flex-row justify-around items-center gap-3 p-4 text-xs font-mono">
          <div className="flex flex-col items-center gap-1 bg-theme-surface border border-theme-border p-2.5 rounded-xl shadow-sm">
            <span className="font-bold text-theme-accent">Server SSR</span>
            <div className="px-1.5 py-0.5 bg-theme-border rounded text-[8px] font-bold">Pre-built HTML</div>
            <span className="text-[8px] text-theme-subtle font-bold">Static Page</span>
          </div>
          <div className="text-theme-accent animate-pulse font-bold text-center">
            <span className="sm:hidden">&#9660; Hydration &#9660;</span>
            <span className="hidden sm:inline">&rarr; Hydration &rarr;</span>
          </div>
          <div className="flex flex-col items-center gap-1 bg-theme-surface border border-theme-border p-2.5 rounded-xl shadow-sm">
            <span className="font-bold text-emerald-500">Client Hydrated</span>
            <div className="px-1.5 py-0.5 bg-emerald-500/20 border border-emerald-500 text-emerald-500 rounded text-[8px] animate-bounce font-bold">Interactive</div>
            <span className="text-[8px] text-theme-subtle font-bold">Active React state</span>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Shipping static layouts before attaching DOM events</span>
      </div>
    );
  }

  // 20. CSS FRAMEWORKS
  if (id === 'css-frameworks' || name.includes('css') || name.includes('tailwind')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Box Model Dimensions</span>
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="border border-dashed border-theme-text/40 p-3 rounded-xl flex items-center justify-center text-[8px] font-mono text-theme-subtle bg-theme-surface">
            Margin
            <div className="border border-theme-accent p-2.5 rounded flex items-center justify-center text-[8px] text-theme-accent bg-theme-accent/10 animate-pulse ml-2.5">
              Padding
              <div className="border border-theme-text/20 p-1.5 rounded bg-theme-bg ml-2.5 text-theme-text font-bold">Content</div>
            </div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Resolving container paddings, borders, and layouts</span>
      </div>
    );
  }

  // 21. HTML, CSS, GIT
  if (id === 'html-css-git' || name.includes('git')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Git Branch DAG Merge</span>
        <div className="flex-1 relative flex items-center justify-center p-4">
          <svg className="w-full h-40 bg-theme-surface border border-theme-border rounded-2xl" style={{ minHeight: '160px' }}>
            <line x1="20%" y1="50%" x2="80%" y2="50%" stroke="var(--color-theme-border)" strokeWidth="3" />
            <path d="M 40 50 C 50 25, 60 25, 70 50" fill="none" stroke="var(--color-theme-accent)" strokeWidth="2.5" strokeDasharray="4" />
            <circle cx="30%" cy="50%" r="8" fill="var(--color-theme-text)" />
            <circle cx="50%" cy="28%" r="8" fill="var(--color-theme-accent)" className="animate-pulse" />
            <circle cx="70%" cy="50%" r="8" fill="#10b981" />
            <circle cx="75%" cy="50%" r="8" fill="#10b981" className="animate-ping" />
          </svg>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Creating branch forks and resolving commit merges</span>
      </div>
    );
  }

  // 22. QUANTITATIVE APTITUDE
  if (id === 'quantitative-aptitude' || name.includes('quantitative') || name.includes('math')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Trigonometric Function Curve</span>
        <div className="flex-1 flex items-center justify-center p-4">
          <svg className="w-24 h-24 stroke-theme-accent fill-none animate-spin-slow" viewBox="0 0 100 100">
            <polygon points="50,10 90,90 10,90" strokeWidth="2" />
            <line x1="50" y1="10" x2="50" y2="90" strokeWidth="1" strokeDasharray="3" />
            <circle cx="50" cy="50" r="3" fill="var(--color-theme-text)" />
          </svg>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Geometric derivations and coordinate systems</span>
      </div>
    );
  }

  // 23. VERBAL APTITUDE
  if (id === 'verbal-aptitude' || name.includes('verbal') || name.includes('reasoning')) {
    return (
      <div className="w-full h-full flex flex-col justify-between">
        <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">Analogy Structure Relationships</span>
        <div className="flex-1 flex flex-col justify-center items-center gap-3 p-4 font-mono text-xs">
          <div className="flex gap-4">
            <div className="px-2 py-1 bg-theme-surface border border-theme-accent text-theme-accent rounded shadow-sm">Hot</div>
            <div className="text-theme-subtle self-center">:</div>
            <div className="px-2 py-1 bg-theme-surface border border-theme-border rounded text-theme-text">Cold</div>
          </div>
          <div className="text-theme-accent font-bold animate-pulse">::</div>
          <div className="flex gap-4">
            <div className="px-2 py-1 bg-theme-surface border border-theme-accent text-theme-accent rounded shadow-sm animate-bounce">Up</div>
            <div className="text-theme-subtle self-center">:</div>
            <div className="px-2 py-1 bg-theme-surface border border-theme-border rounded text-theme-text">Down</div>
          </div>
        </div>
        <span className="text-xs font-mono text-theme-subtle text-center pb-2">Analyzing semantics, logical structures, and synonyms</span>
      </div>
    );
  }

  // Default fallback
  return (
    <div className="w-full h-full flex flex-col justify-between">
      <span className="text-xs font-mono text-theme-accent uppercase font-bold text-center mt-2">AST Parsing Tree</span>
      <div className="flex-1 flex flex-col justify-center items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-theme-accent/10 border border-theme-accent/20 flex items-center justify-center text-theme-accent animate-pulse">
          <Code size={16} />
        </div>
        <span className="text-[10px] font-mono text-theme-text">{"Program Statement -> Variable Declaration"}</span>
      </div>
      <span className="text-xs font-mono text-theme-subtle text-center pb-2">Parsing statement nodes into operational hierarchies</span>
    </div>
  );
}
