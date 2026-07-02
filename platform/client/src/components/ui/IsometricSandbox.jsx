import React, { useState } from 'react';

/**
 * IsometricSandbox renders a 3D isometric stack visualization
 * where users can push/pop items and tilt the viewport by moving
 * the mouse cursor across the container.
 */
export default function IsometricSandbox() {
  const [stack, setStack] = useState(['AST Node', 'Scope Frame', 'Class Instance']);
  const [tiltX, setTiltX] = useState(60);
  const [tiltZ, setTiltZ] = useState(-45);

  const pushStack = () => {
    if (stack.length >= 6) return;
    const items = ['Symbol Scope', 'Pointer Ref', 'Heap Block', 'Thread Frame', 'Mutex Lock', 'Sys Call', 'B-Tree Node'];
    const randomItem = items[Math.floor(Math.random() * items.length)];
    setStack([randomItem, ...stack]);
  };

  const popStack = () => {
    if (stack.length === 0) return;
    setStack(stack.slice(1));
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

  const stackColors = [
    { bg: 'bg-theme-accent', sideL: 'bg-theme-accent/80', sideF: 'bg-theme-accent/60', text: 'text-white' },
    { bg: 'bg-emerald-500', sideL: 'bg-emerald-600', sideF: 'bg-emerald-700', text: 'text-white' },
    { bg: 'bg-amber-500', sideL: 'bg-amber-600', sideF: 'bg-amber-700', text: 'text-white' },
    { bg: 'bg-indigo-500', sideL: 'bg-indigo-600', sideF: 'bg-indigo-700', text: 'text-white' },
    { bg: 'bg-cyan-500', sideL: 'bg-cyan-600', sideF: 'bg-cyan-700', text: 'text-white' },
    { bg: 'bg-rose-500', sideL: 'bg-rose-600', sideF: 'bg-rose-700', text: 'text-white' }
  ];

  return (
    <section id="interactive-sandbox" className="scroll-mt-[120px] py-24 bg-theme-surface/40 border-y border-theme-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left: Info panel */}
          <div className="space-y-6">
            <span className="text-[10px] font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-3 py-1 rounded-full">
              Interactive 3D Sandbox
            </span>
            <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text leading-tight">
              Play in 3D: <br />
              Visualize Data Structures
            </h2>
            <p className="text-theme-subtle text-sm leading-relaxed">
              Interact with compilation stack scopes and data pipelines in full isometric 3D space. Move your mouse across the viewport to tilt the workspace, inspecting depth boundaries in real time.
            </p>
            
            <div className="flex gap-4">
              <button 
                onClick={pushStack}
                className="bg-theme-accent hover:opacity-90 text-white font-bold px-5 py-2.5 rounded-xl shadow-md transition-all active:scale-95 text-xs cursor-pointer"
              >
                Push Item
              </button>
              <button 
                onClick={popStack}
                className="border border-theme-border hover:bg-theme-border text-theme-text font-bold px-5 py-2.5 rounded-xl transition-all active:scale-95 text-xs cursor-pointer"
              >
                Pop Item
              </button>
            </div>
          </div>

          {/* Right: 3D Viewport */}
          <div className="flex items-center justify-center">
            <div 
              className="w-full max-w-[420px] h-[340px] bg-theme-surface border border-theme-border rounded-2xl flex items-center justify-center relative overflow-hidden shadow-lg cursor-grab active:cursor-grabbing"
              onMouseMove={handleMouseMove}
              onMouseLeave={handleMouseLeave}
              style={{ perspective: '800px' }}
            >
              {/* Visual grid reference lines */}
              <div className="absolute inset-0 bg-[radial-gradient(var(--color-border)_1px,transparent_1px)] [background-size:16px_16px] opacity-40" />

              {/* 3D Stack container (Anchored to the bottom) */}
              <div 
                className="absolute bottom-12 flex flex-col-reverse items-center justify-center w-full"
                style={{
                  transformStyle: 'preserve-3d',
                  transform: `rotateX(${tiltX}deg) rotateZ(${tiltZ}deg)`,
                  transition: 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
                }}
              >
                {/* 3D Glass Outline Stack Chamber/Pillars */}
                <div 
                  className="absolute w-32 h-48 border border-dashed border-theme-border/60 rounded-xl"
                  style={{
                    transformStyle: 'preserve-3d',
                    transform: 'translate3d(-50%, -50%, 64px)',
                  }}
                />

                {/* Base Plate */}
                <div 
                  className="absolute w-28 h-28 left-1/2 top-1/2 bg-theme-border/80 border border-theme-border rounded-lg shadow-inner flex items-center justify-center font-mono text-[9px] font-bold text-theme-subtle"
                  style={{ 
                    transform: 'translate3d(-50%, -50%, 0px)', 
                    transformStyle: 'preserve-3d' 
                  }}
                >
                  STACK BASE
                </div>

                 {/* 3D Floating Layers */}
                {stack.map((item, idx) => {
                  const color = stackColors[idx % stackColors.length];
                  return (
                    <div 
                      key={idx}
                      className="absolute w-24 h-24 left-1/2 top-1/2 transition-all duration-500 ease-out" 
                      style={{ 
                        transformStyle: 'preserve-3d',
                        transform: `translate3d(-50%, -50%, ${(idx + 1) * 28}px)`,
                      }}
                    >
                      {/* Top Face */}
                      <div className={`absolute inset-0 border border-theme-bg/25 rounded-md flex items-center justify-center font-mono font-bold text-[9px] shadow-lg select-none ${color.bg} ${color.text}`} style={{ transform: 'translateZ(12px)' }}>
                        {item}
                      </div>
                      {/* Left Face */}
                      <div className={`absolute left-0 top-0 bottom-0 w-[12px] origin-left ${color.sideL}`} style={{ transform: 'rotateY(-90deg)' }} />
                      {/* Front Face */}
                      <div className={`absolute left-0 right-0 bottom-0 h-[12px] origin-bottom ${color.sideF}`} style={{ transform: 'rotateX(-90deg)' }} />
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
