import React, { useState, useEffect, useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const sections = [
  { id: 'hero-section', label: 'Home' },
  { id: 'visual-pedagogy', label: 'Pedagogy' },
  { id: 'curriculum-grid', label: 'Roadmap' },
  { id: 'interactive-sandbox', label: '3D Sandbox' },
  { id: 'ai-profiling', label: 'AI Profiling' },
  { id: 'learning-features', label: 'Features' }
];

export default function SecondaryNavbar() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [canScrollLeft, setCanScrollLeft]   = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);
  const scrollRef = useRef(null);
  const dotRefs   = useRef([]);

  // ── Page-scroll → progress ─────────────────────────────────────────────
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const viewportH = window.innerHeight;

      const positions = sections.map(sec => {
        const el = document.getElementById(sec.id);
        return el ? el.offsetTop - 120 : 0;
      });

      const maxScroll    = document.documentElement.scrollHeight - viewportH;
      const currentScroll = Math.min(scrollTop, maxScroll);

      let progress = 0;
      for (let i = 0; i < positions.length - 1; i++) {
        const start = positions[i];
        const end   = positions[i + 1];
        if (currentScroll >= start && currentScroll < end) {
          progress = i + (currentScroll - start) / (end - start);
          break;
        } else if (currentScroll >= end) {
          progress = i + 1;
        }
      }
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // ── Auto-scroll active dot into view on mobile ─────────────────────────
  useEffect(() => {
    const activeIdx = Math.round(scrollProgress);
    const dot       = dotRefs.current[activeIdx];
    const container = scrollRef.current;
    if (!dot || !container) return;
    const target = dot.offsetLeft + dot.offsetWidth / 2 - container.clientWidth / 2;
    container.scrollTo({ left: target, behavior: 'smooth' });
  }, [Math.round(scrollProgress)]);

  // ── Edge-fade indicators ───────────────────────────────────────────────
  const updateEdges = () => {
    const el = scrollRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 4);
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 4);
  };

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    updateEdges();
    el.addEventListener('scroll', updateEdges, { passive: true });
    window.addEventListener('resize', updateEdges);
    return () => {
      el.removeEventListener('scroll', updateEdges);
      window.removeEventListener('resize', updateEdges);
    };
  }, []);

  // ── Smooth nav click ───────────────────────────────────────────────────
  const handleNavClick = (id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const start    = window.pageYOffset || document.documentElement.scrollTop;
    const target   = el.getBoundingClientRect().top + start - 120;
    const distance = target - start;
    const ease     = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2;
    const dur      = 1200;
    let t0 = null;
    const step = (now) => {
      if (!t0) t0 = now;
      const ratio = ease(Math.min((now - t0) / dur, 1));
      window.scrollTo(0, start + distance * ratio);
      if (now - t0 < dur) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const progressPercent = (scrollProgress / (sections.length - 1)) * 100;

  return (
    <div className="fixed top-16 left-0 right-0 z-40 bg-gradient-to-b from-theme-bg via-theme-bg/85 to-transparent backdrop-blur-sm h-16 flex items-center select-none w-full">

      {/* Ambient glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[400px] h-[3px] bg-theme-accent/20 blur-[4px] rounded-full pointer-events-none" />
      <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-72 h-16 bg-theme-accent/5 blur-2xl rounded-full pointer-events-none -z-10" />

      {/* ── Left edge fade ──────────────────────────────────────────────── */}
      <div
        aria-hidden="true"
        className={`absolute left-0 top-0 bottom-0 z-20 w-12 flex items-center justify-start pl-1.5 pointer-events-none transition-opacity duration-300 ${canScrollLeft ? 'opacity-100' : 'opacity-0'}`}
        style={{ background: 'linear-gradient(to right, var(--color-bg) 30%, transparent 100%)' }}
      >
        <ChevronLeft size={13} className="text-theme-subtle" />
      </div>

      {/* ── Scrollable container ────────────────────────────────────────── */}
      <div
        ref={scrollRef}
        className="w-full overflow-x-auto flex items-center min-w-0 px-4"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {/*
          KEY LAYOUT FIX:
          We split dots and labels into two separate rows inside a flex-col
          wrapper, so the "dots row" stands alone with its own height.
          The track line sits inside the dots row with top-1/2 -translate-y-1/2,
          guaranteeing it passes through the geometric centre of every dot.
          No more guesswork with pixel offsets.
        */}
        <div
          id="secondary-nav-container"
          className="flex flex-col items-stretch shrink-0 w-full min-w-[560px] max-w-2xl mx-auto"
        >
          {/* ── Row 1: dots + track line ─────────────────────────────── */}
          <div className="relative flex items-center justify-between w-full">

            {/* Track line — inside the dots row, top-1/2 aligns with dot centres */}
            <div
              className="absolute left-5 right-5 h-[2px] top-1/2 -translate-y-1/2 bg-theme-border/40 z-0 rounded-full"
              aria-hidden="true"
            >
              <div
                className="h-full bg-theme-accent rounded-full"
                style={{
                  width: `${progressPercent}%`,
                  boxShadow: '0 0 6px var(--color-accent)'
                }}
              />
            </div>

            {/* Dots */}
            {sections.map((sec, idx) => {
              const isPassed = scrollProgress >= idx;
              return (
                <button
                  key={sec.id}
                  ref={el => (dotRefs.current[idx] = el)}
                  onClick={() => handleNavClick(sec.id)}
                  className="relative z-10 flex items-center justify-center w-10 h-5 cursor-pointer focus:outline-none group"
                  aria-label={`Navigate to ${sec.label}`}
                >
                  <div
                    className={`w-3 h-3 rounded-full border-2 transition-all duration-300 shrink-0 ${
                      isPassed
                        ? 'bg-theme-accent border-theme-bg scale-110'
                        : 'bg-theme-bg border-theme-subtle group-hover:border-theme-accent'
                    }`}
                    style={isPassed ? { boxShadow: '0 0 6px var(--color-accent)' } : {}}
                  />
                </button>
              );
            })}
          </div>

          {/* ── Row 2: labels — each aligned under its dot ───────────── */}
          <div className="flex items-start justify-between w-full mt-1">
            {sections.map((sec, idx) => {
              const isPassed = scrollProgress >= idx;
              const isActive = Math.round(scrollProgress) === idx;
              return (
                <button
                  key={sec.id}
                  onClick={() => handleNavClick(sec.id)}
                  className="flex justify-center w-10 cursor-pointer focus:outline-none group hover:scale-[1.05] transition-transform duration-200"
                >
                  <span
                    className={`text-[10px] sm:text-[11px] font-mono tracking-wide font-bold whitespace-nowrap leading-none transition-colors duration-200 ${
                      isActive
                        ? 'text-theme-accent'
                        : isPassed
                          ? 'text-theme-text opacity-90'
                          : 'text-theme-subtle opacity-60 group-hover:opacity-100'
                    }`}
                  >
                    {sec.label}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Right edge fade ─────────────────────────────────────────────── */}
      <div
        aria-hidden="true"
        className={`absolute right-0 top-0 bottom-0 z-20 w-12 flex items-center justify-end pr-1.5 pointer-events-none transition-opacity duration-300 ${canScrollRight ? 'opacity-100' : 'opacity-0'}`}
        style={{ background: 'linear-gradient(to left, var(--color-bg) 30%, transparent 100%)' }}
      >
        <ChevronRight size={13} className="text-theme-subtle" />
      </div>
    </div>
  );
}
