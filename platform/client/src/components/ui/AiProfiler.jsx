import React, { useState, useEffect } from 'react';

/**
 * AiProfiler renders the AI diagnostics terminal console section
 * with a live typewriter effect for terminal logs, dynamic cognitive
 * metrics progress bars, and a scan execution button.
 */
export default function AiProfiler() {
  const [metrics, setMetrics] = useState({ cognitive: 87, retention: 92, recall: 78 });
  const [terminalLogs, setTerminalLogs] = useState([
    '[system] Profiler kernel active on core-0.',
    '[system] Traced 4 scopes; cognitive coherence at 87%.'
  ]);
  const [currentTypingText, setCurrentTypingText] = useState('');

  const runScan = () => {
    setMetrics({
      cognitive: Math.floor(Math.random() * 15) + 82,
      retention: Math.floor(Math.random() * 15) + 82,
      recall: Math.floor(Math.random() * 20) + 75
    });
    setTerminalLogs(prev => [
      ...prev.slice(-3),
      `[profiler] Scanning conceptual traces... Done.`,
      `[profiler] Retention profile updated.`
    ]);
  };

  useEffect(() => {
    const events = [
      '[profiler] Traced conceptual leak in DBMS transaction concurrency control.',
      '[profiler] Memory recall index for "Thread Scheduling Algorithms" elevated.',
      '[ai-copilot] Generated micro-lesson challenge: "Math behind Backpropagation".',
      '[system] Synchronizing local study logs with MongoDB Atlas replica set...',
      '[system] Log database successfully updated.',
      '[profiler] AI agent profiled: Weakness found in "B+ Tree Disk Seeks".'
    ];
    let eventIdx = 0;

    const typeWriterTimer = (text, charIdx, callback) => {
      if (charIdx < text.length) {
        setCurrentTypingText(text.slice(0, charIdx + 1));
        setTimeout(() => typeWriterTimer(text, charIdx + 1, callback), 30);
      } else {
        callback();
      }
    };

    const triggerNextLog = () => {
      const nextText = events[eventIdx];
      eventIdx = (eventIdx + 1) % events.length;
      typeWriterTimer(nextText, 0, () => {
        setTerminalLogs(prev => [...prev.slice(-3), nextText]);
        setCurrentTypingText('');
        setTimeout(triggerNextLog, 3000);
      });
    };

    const startTimeout = setTimeout(triggerNextLog, 2000);
    return () => clearTimeout(startTimeout);
  }, []);

  return (
    <section id="ai-profiling" className="scroll-mt-[120px] py-24 bg-theme-surface/10 border-b border-theme-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left: Terminal console */}
          <div className="bg-theme-surface border border-theme-border rounded-2xl p-6 shadow-lg font-mono text-xs flex flex-col justify-between h-[340px] w-full max-w-[480px] mx-auto relative overflow-hidden">
            {/* Scanline overlay for high-end macOS terminal styling */}
            <div className="absolute inset-0 bg-gradient-to-b from-theme-text/5 to-transparent pointer-events-none z-10 opacity-30 animate-pulse" />
            
            <div className="flex items-center justify-between pb-3 border-b border-theme-border select-none">
              <div className="flex gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-green-500/80 animate-pulse" />
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-ping" />
                <span className="text-[10px] font-bold text-theme-subtle">ascendrite-ai-profiler --v1.0.0</span>
              </div>
            </div>
            
            <div className="flex-1 py-4 overflow-y-auto space-y-2 text-theme-text font-semibold text-[11px] leading-relaxed select-text relative z-20">
              {terminalLogs.map((log, idx) => (
                <div key={idx}>
                  <span className="text-theme-accent select-none">&gt;&gt;</span> {log}
                </div>
              ))}
              {currentTypingText && (
                <div>
                  <span className="text-theme-accent select-none">&gt;&gt;</span> {currentTypingText}
                  <span className="animate-pulse font-bold text-theme-accent ml-0.5">&#9611;</span>
                </div>
              )}
              {!currentTypingText && (
                <div>
                  <span className="text-theme-accent select-none">&gt;&gt;</span>
                  <span className="animate-pulse font-bold text-theme-accent ml-0.5">&#9611;</span>
                </div>
              )}
            </div>
            
            <button 
              onClick={runScan}
              className="w-full bg-theme-border border border-theme-border hover:bg-theme-surface text-theme-text font-bold py-2 rounded-xl text-xs transition-all active:scale-95 cursor-pointer"
            >
              Execute Assessment Scan
            </button>
          </div>

          {/* Right: Info panel & dynamic stats */}
          <div className="space-y-6">
            <span className="text-[10px] font-bold text-theme-accent uppercase tracking-wider bg-theme-accent/15 px-3 py-1 rounded-full">
              AI Diagnostics
            </span>
            <h2 className="font-display font-bold text-3xl sm:text-4xl text-theme-text leading-tight">
              Dynamic Cognitive <br />
              Profiling & Feedback
            </h2>
            <p className="text-theme-subtle text-sm leading-relaxed">
              Ascendrite's AI agent traces your path step completion intervals and assessment score distributions to compute a localized conceptual recall profile.
            </p>

            {/* Dynamic metrics bar counters */}
            <div className="space-y-4 pt-2">
              <div>
                <div className="flex justify-between text-xs font-bold text-theme-text mb-1">
                  <span>Cognitive Coherence</span>
                  <span className="text-theme-accent">{metrics.cognitive}%</span>
                </div>
                <div className="h-1.5 w-full bg-theme-border rounded-full overflow-hidden">
                  <div className="h-full bg-theme-accent transition-all duration-500" style={{ width: `${metrics.cognitive}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs font-bold text-theme-text mb-1">
                  <span>Concept Retention</span>
                  <span className="text-theme-accent">{metrics.retention}%</span>
                </div>
                <div className="h-1.5 w-full bg-theme-border rounded-full overflow-hidden">
                  <div className="h-full bg-theme-accent transition-all duration-500" style={{ width: `${metrics.retention}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs font-bold text-theme-text mb-1">
                  <span>Recall Rate</span>
                  <span className="text-theme-accent">{metrics.recall}%</span>
                </div>
                <div className="h-1.5 w-full bg-theme-border rounded-full overflow-hidden">
                  <div className="h-full bg-theme-accent transition-all duration-500" style={{ width: `${metrics.recall}%` }} />
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
