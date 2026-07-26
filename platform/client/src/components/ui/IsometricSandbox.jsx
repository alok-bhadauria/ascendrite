import React, { useState } from 'react';

/**
 * IsometricSandbox renders a 3D memory heap allocator simulator.
 * Users can malloc/free memory blocks on a 3x3 virtual heap arena,
 * tilting the isometric grid via mouse mouseovers.
 */
export default function IsometricSandbox() {
  const [memory, setMemory] = useState([
    { id: 0, addr: '0x00', label: 'AST Node', size: '16B', allocated: true, color: 0 },
    { id: 1, addr: '0x04', label: 'Scope Frame', size: '32B', allocated: true, color: 1 },
    { id: 2, addr: '0x08', label: '', size: '0B', allocated: false, color: 0 },
    { id: 3, addr: '0x0C', label: 'Class Ptr', size: '64B', allocated: true, color: 2 },
    { id: 4, addr: '0x10', label: '', size: '0B', allocated: false, color: 0 },
    { id: 5, addr: '0x14', label: '', size: '0B', allocated: false, color: 0 },
    { id: 6, addr: '0x18', label: 'Mutex Lock', size: '8B', allocated: true, color: 3 },
    { id: 7, addr: '0x1C', label: '', size: '0B', allocated: false, color: 0 },
    { id: 8, addr: '0x20', label: '', size: '0B', allocated: false, color: 0 }
  ]);

  const [tiltX, setTiltX] = useState(60);
  const [tiltZ, setTiltZ] = useState(-45);
  const [terminalLog, setTerminalLog] = useState('sys_heap_init: allocated 4 descriptors.');

  const runMalloc = () => {
    const freeBlocks = memory.filter(b => !b.allocated);
    if (freeBlocks.length === 0) {
      setTerminalLog('malloc: OOM (Out Of Memory) - failed to allocate heap sector.');
      return;
    }
    const targetBlock = freeBlocks[Math.floor(Math.random() * freeBlocks.length)];
    const types = [
      { label: 'Buffer', size: '128B', color: 4 },
      { label: 'Socket Ref', size: '16B', color: 5 },
      { label: 'File Desc', size: '8B', color: 1 },
      { label: 'Heap Chunk', size: '64B', color: 3 },
      { label: 'Symbol Val', size: '32B', color: 2 }
    ];
    const chosen = types[Math.floor(Math.random() * types.length)];

    setMemory(prev => prev.map(b => b.id === targetBlock.id ? { 
      ...b, 
      allocated: true, 
      label: chosen.label, 
      size: chosen.size,
      color: chosen.color
    } : b));

    setTerminalLog(`void* ptr = malloc(${chosen.size.replace('B', '')}); // assigned cell index ${targetBlock.id} at ${targetBlock.addr}`);
  };

  const runFree = () => {
    const allocatedBlocks = memory.filter(b => b.allocated);
    if (allocatedBlocks.length === 0) {
      setTerminalLog('free: null pointer assignment - no sectors allocated.');
      return;
    }
    const targetBlock = allocatedBlocks[allocatedBlocks.length - 1];

    setMemory(prev => prev.map(b => b.id === targetBlock.id ? { 
      ...b, 
      allocated: false, 
      label: '', 
      size: '0B'
    } : b));

    setTerminalLog(`free(${targetBlock.addr}); // released heap block memory descriptor`);
  };

  const handleMouseMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    setTiltX(60 - (y / rect.height) * 15);
    setTiltZ(-45 + (x / rect.width) * 20);
  };

  const handleMouseLeave = () => {
    setTiltX(60);
    setTiltZ(-45);
  };

  const blockColors = [
    { bg: 'bg-theme-accent', sideL: 'bg-theme-accent/80', sideF: 'bg-theme-accent/60', text: 'text-white' },
    { bg: 'bg-emerald-500', sideL: 'bg-emerald-600', sideF: 'bg-emerald-700', text: 'text-white' },
    { bg: 'bg-amber-500', sideL: 'bg-amber-600', sideF: 'bg-amber-700', text: 'text-white' },
    { bg: 'bg-indigo-500', sideL: 'bg-indigo-600', sideF: 'bg-indigo-700', text: 'text-white' },
    { bg: 'bg-cyan-500', sideL: 'bg-cyan-600', sideF: 'bg-cyan-700', text: 'text-white' },
    { bg: 'bg-rose-500', sideL: 'bg-rose-600', sideF: 'bg-rose-700', text: 'text-white' }
  ];

  return (
    <section id="interactive-sandbox" className="scroll-mt-[120px] py-24 bg-theme-surface/30 border-y border-theme-border/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left: Metadata Descriptions */}
          <div className="lg:col-span-5 space-y-6">
            <span className="text-[10px] font-mono font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/10 border border-theme-accent/20 px-3.5 py-1 rounded-full">
              Heap Space Visualizer
            </span>
            <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-theme-text leading-tight tracking-tight">
              3D Heap Allocation Arena
            </h2>
            <p className="text-theme-subtle text-sm leading-relaxed">
              Step into physical execution memory. Play with dynamic allocations inside virtual pages. Move your mouse to pivot the isometric layout, observing malloc and free boundaries in real time.
            </p>
            
            <div className="flex gap-3">
              <button 
                onClick={runMalloc}
                className="bg-theme-accent hover:opacity-90 hover:scale-[1.02] hover:shadow-md text-white font-bold px-5 py-2.5 rounded-xl shadow-md transition-all active:scale-[0.98] text-xs cursor-pointer"
              >
                malloc() Allocation
              </button>
              <button 
                onClick={runFree}
                className="border border-theme-border hover:bg-theme-border text-theme-text font-bold px-5 py-2.5 rounded-xl transition-all active:scale-[0.98] text-xs cursor-pointer"
              >
                free() Release
              </button>
            </div>

            {/* Simulated Debug console readout */}
            <div className="bg-theme-bg border border-theme-border rounded-xl p-4 font-mono text-[11px] text-theme-text select-all space-y-1">
              <span className="text-theme-accent block font-bold"># terminal logger output:</span>
              <span className="opacity-80 block">&gt;&gt; {terminalLog}</span>
            </div>
          </div>

          {/* Right: 3D Viewport */}
          <div className="lg:col-span-7 flex items-center justify-center">
            <div 
              className="w-full max-w-[480px] h-[380px] bg-theme-surface/50 border border-theme-border rounded-3xl flex items-center justify-center relative overflow-hidden shadow-xl"
              onMouseMove={handleMouseMove}
              onMouseLeave={handleMouseLeave}
              style={{ perspective: '1000px' }}
            >
              {/* Reference Grid lines */}
              <div className="absolute inset-0 bg-[radial-gradient(var(--color-border)_1px,transparent_1px)] [background-size:24px_24px] opacity-40 pointer-events-none" />

              {/* 3D Grid Arena */}
              <div 
                className="absolute flex items-center justify-center w-80 h-80"
                style={{
                  transformStyle: 'preserve-3d',
                  transform: `rotateX(${tiltX}deg) rotateZ(${tiltZ}deg)`,
                  transition: 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
                }}
              >
                {/* 3D Base Plate container */}
                <div className="grid grid-cols-3 gap-6 p-4 bg-theme-bg/60 border border-theme-border rounded-2xl w-72 h-72 relative">
                  
                  {memory.map((block) => {
                    const r = Math.floor(block.id / 3);
                    const c = block.id % 3;
                    const xOffset = (c - 1) * 80;
                    const yOffset = (r - 1) * 80;

                    const color = blockColors[block.color % blockColors.length];

                    return (
                      <div 
                        key={block.id}
                        className="absolute w-16 h-16 transition-all duration-500 ease-out"
                        style={{
                          transformStyle: 'preserve-3d',
                          left: '50%',
                          top: '50%',
                          transform: `translate3d(calc(-50% + ${xOffset}px), calc(-50% + ${yOffset}px), 0px)`
                        }}
                      >
                        {/* Wireframe Placeholder Cell */}
                        <div 
                          className="absolute inset-0 border border-dashed border-theme-border/70 rounded-lg flex flex-col justify-between p-1.5 font-mono text-[8px] text-theme-subtle select-none bg-theme-surface/10"
                        >
                          <span>{block.addr}</span>
                          <span className="text-right">#0{block.id}</span>
                        </div>

                        {/* Solid 3D Box (pops up when allocated) */}
                        {block.allocated && (
                          <div 
                            className="absolute inset-0 transition-transform duration-500 ease-out animate-fade-in"
                            style={{ 
                              transformStyle: 'preserve-3d',
                              transform: 'translateZ(12px)'
                            }}
                          >
                            {/* Top Face */}
                            <div className={`absolute inset-0 border border-theme-bg/15 rounded-lg flex flex-col justify-between p-2 font-mono text-white select-none ${color.bg} shadow-md`}>
                              <span className="text-[8px] font-bold opacity-80">{block.addr}</span>
                              <span className="text-[9px] font-extrabold truncate">{block.label}</span>
                              <span className="text-[8px] opacity-75 text-right">{block.size}</span>
                            </div>
                            
                            {/* Left Side Face */}
                            <div 
                              className={`absolute left-0 top-0 bottom-0 w-[12px] origin-left rounded-l-md ${color.sideL}`} 
                              style={{ transform: 'rotateY(-90deg) translateZ(0px)' }} 
                            />
                            
                            {/* Front Side Face */}
                            <div 
                              className={`absolute left-0 right-0 bottom-0 h-[12px] origin-bottom rounded-b-md ${color.sideF}`} 
                              style={{ transform: 'rotateX(-90deg) translateZ(0px)' }} 
                            />
                          </div>
                        )}
                      </div>
                    );
                  })}
                  
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
