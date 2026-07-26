import React, { useState, useEffect, useRef } from 'react';
import { FaPlay, FaPause, FaStepForward, FaUndo } from 'react-icons/fa';

export default function InteractiveVisualizerDemo() {
  const initialArr = [
    { id: 45, val: 45, index: 0 },
    { id: 18, val: 18, index: 1 },
    { id: 85, val: 85, index: 2 },
    { id: 32, val: 32, index: 3 },
    { id: 64, val: 64, index: 4 },
    { id: 12, val: 12, index: 5 },
    { id: 53, val: 53, index: 6 }
  ];

  const [arrayState, setArrayState] = useState(initialArr);
  const [activeIndices, setActiveIndices] = useState([]);
  const [sortedCount, setSortedCount] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeLine, setActiveLine] = useState(0);
  
  const timerRef = useRef(null);
  const stateRef = useRef({ i: 0, j: 0, swapped: false });

  const resetVisualizer = () => {
    setIsPlaying(false);
    if (timerRef.current) clearInterval(timerRef.current);
    setArrayState(initialArr);
    setActiveIndices([]);
    setSortedCount(0);
    setActiveLine(0);
    stateRef.current = { i: 0, j: 0, swapped: false };
  };

  const stepBubbleSort = () => {
    let { i, j } = stateRef.current;
    const n = arrayState.length;

    if (i >= n - 1) {
      setIsPlaying(false);
      setSortedCount(n);
      setActiveIndices([]);
      setActiveLine(0);
      return;
    }

    // Step 1: Highlight comparison
    setActiveIndices([j, j + 1]);
    setActiveLine(3); // Highlights 'if arr[j] > arr[j+1]' line

    // Step 2: Perform the comparison and potential swap
    setTimeout(() => {
      // Find items at current positions j and j + 1
      const itemA = arrayState.find(item => item.index === j);
      const itemB = arrayState.find(item => item.index === j + 1);

      if (itemA && itemB && itemA.val > itemB.val) {
        // Swap indices inside arrayState
        setArrayState(prev => prev.map(item => {
          if (item.id === itemA.id) return { ...item, index: j + 1 };
          if (item.id === itemB.id) return { ...item, index: j };
          return item;
        }));
        setActiveLine(4); // Highlights swap assignment line
        stateRef.current.swapped = true;
      } else {
        setActiveLine(2); // Highlights loop check
      }

      // Step 3: Advance search index j
      setTimeout(() => {
        let nextJ = j + 1;
        let nextI = i;
        let nextSwapped = stateRef.current.swapped;

        if (nextJ >= n - i - 1) {
          nextJ = 0;
          nextI++;
          setSortedCount(nextI);
          nextSwapped = false;
        }

        stateRef.current = { i: nextI, j: nextJ, swapped: nextSwapped };
        
        if (nextI >= n - 1) {
          setSortedCount(n);
          setActiveIndices([]);
          setActiveLine(0);
          setIsPlaying(false);
        } else {
          setActiveIndices([nextJ, nextJ + 1]);
          setActiveLine(2);
        }
      }, 500);

    }, 450);
  };

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        stepBubbleSort();
      }, 1200);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, arrayState]);

  return (
    <div className="bg-theme-surface border border-theme-border rounded-xl p-6 shadow-xl w-full max-w-3xl mx-auto flex flex-col md:flex-row gap-6 relative select-none">
      {/* Visualizer Canvas Area */}
      <div className="flex-1 flex flex-col justify-between">
        <div>
          <h4 className="font-display font-bold text-lg text-theme-accent mb-1">Sorting steps simulator</h4>
          <p className="text-xs text-theme-subtle mb-4">Observe how memory operations map to code lines in real-time.</p>
        </div>

        {/* Absolute-positioned slide bars container */}
        <div className="h-44 relative w-full border-b border-theme-border pb-2 justify-center overflow-hidden">
          {arrayState.map((item) => {
            const isComparing = activeIndices.includes(item.index);
            const isSorted = item.index >= arrayState.length - sortedCount;
            let barColor = 'bg-theme-subtle opacity-60';
            if (isComparing) barColor = 'bg-theme-accent shadow-[0_0_12px_var(--color-theme-accent)]';
            else if (isSorted) barColor = 'bg-emerald-500 opacity-90';
            
            // Calculate dynamic left offset relative to active sorted position index
            const leftPercent = item.index * (100 / 7);

            return (
              <div 
                key={item.id} 
                className="absolute bottom-2 flex flex-col items-center transition-all duration-500 ease-in-out"
                style={{ 
                  width: '11%', 
                  left: `${leftPercent}%`, 
                  height: '80%', 
                  justifyContent: 'flex-end'
                }}
              >
                <span className="text-[10px] mb-1 font-mono text-theme-text transition-colors duration-300">
                  {item.val}
                </span>
                <div 
                  className={`w-full rounded-t-sm transition-all duration-300 ${barColor}`}
                  style={{ height: `${item.val * 1.3}px` }}
                />
              </div>
            );
          })}
        </div>
        
        {/* Visualizer Controls */}
        <div className="flex flex-wrap gap-2.5 sm:gap-4 mt-6 justify-center">
          <button 
            id="btn-play-viz"
            onClick={() => setIsPlaying(!isPlaying)} 
            className="flex items-center gap-1.5 sm:gap-2 bg-theme-accent hover:opacity-90 text-white font-semibold px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg transition-all shadow-md active:scale-95 text-xs sm:text-sm cursor-pointer"
          >
            {isPlaying ? <FaPause size={12} /> : <FaPlay size={12} />}
            <span>{isPlaying ? 'Pause' : 'Auto Play'}</span>
          </button>
          <button 
            id="btn-step-viz"
            onClick={stepBubbleSort} 
            disabled={isPlaying}
            className="flex items-center gap-1.5 sm:gap-2 border border-theme-border hover:bg-theme-border text-theme-text font-semibold px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg disabled:opacity-40 transition-all active:scale-95 text-xs sm:text-sm cursor-pointer"
          >
            <FaStepForward size={12} />
            <span>Step</span>
          </button>
          <button 
            id="btn-reset-viz"
            onClick={resetVisualizer}
            className="flex items-center gap-1.5 sm:gap-2 border border-theme-border hover:bg-theme-border text-theme-text font-semibold px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg transition-all active:scale-95 text-xs sm:text-sm cursor-pointer"
          >
            <FaUndo size={12} />
            <span>Reset</span>
          </button>
        </div>
      </div>

      {/* Python Code Trace Area */}
      <div className="w-full md:w-80 bg-theme-bg border border-theme-border rounded-lg p-4 font-mono text-xs select-none overflow-x-auto">
        <div className="text-theme-subtle text-[10px] uppercase tracking-wider mb-3 font-bold">Python Code Trace</div>
        <div className="flex flex-col gap-1.5">
          {[
            "def bubble_sort(arr):",
            "    for i in range(len(arr)):",
            "        for j in range(len(arr)-i-1):",
            "            if arr[j] > arr[j+1]:",
            "                arr[j], arr[j+1] = arr[j+1], arr[j]"
          ].map((line, idx) => {
            const isHighlighted = idx === activeLine;
            return (
              <div 
                key={idx} 
                className={`py-1 px-2.5 rounded whitespace-pre transition-all duration-200 border-l-2 ${
                  isHighlighted 
                    ? 'text-theme-accent font-bold border-theme-accent shadow-sm' 
                    : 'text-theme-text border-transparent opacity-55'
                }`}
                style={isHighlighted ? { backgroundColor: 'color-mix(in srgb, var(--color-theme-accent) 12%, transparent)' } : {}}
              >
                {line}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
