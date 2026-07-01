import React, { useState, useEffect, useRef } from 'react';
import { FaPlay, FaPause, FaStepForward, FaUndo } from 'react-icons/fa';

export default function InteractiveVisualizerDemo() {
  const [array, setArray] = useState([45, 18, 85, 32, 64, 12, 53]);
  const [activeIndices, setActiveIndices] = useState([]);
  const [sortedCount, setSortedCount] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeLine, setActiveLine] = useState(0);
  const timerRef = useRef(null);

  // Reference for tracking state variables across async ticks
  const stateRef = useRef({
    i: 0,
    j: 0,
    swapped: false,
    arr: [45, 18, 85, 32, 64, 12, 53]
  });

  const resetVisualizer = () => {
    setIsPlaying(false);
    if (timerRef.current) clearInterval(timerRef.current);
    const initialArr = [45, 18, 85, 32, 64, 12, 53];
    setArray(initialArr);
    setActiveIndices([]);
    setSortedCount(0);
    setActiveLine(0);
    stateRef.current = {
      i: 0,
      j: 0,
      swapped: false,
      arr: [...initialArr]
    };
  };

  const stepBubbleSort = () => {
    let { i, j, swapped, arr } = stateRef.current;
    const n = arr.length;

    if (i >= n - 1) {
      setIsPlaying(false);
      setSortedCount(n);
      setActiveIndices([]);
      setActiveLine(0);
      return;
    }

    // Step 1: Highlight comparison
    setActiveIndices([j, j + 1]);
    setActiveLine(3); // Highlights if condition checking line

    setTimeout(() => {
      // Step 2: Swap values if needed
      if (arr[j] > arr[j + 1]) {
        const temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        setArray([...arr]);
        setActiveLine(4); // Highlights swap assignment line
        stateRef.current.swapped = true;
      } else {
        setActiveLine(2); // Highlights loop increment check line
      }

      // Step indices increment
      j++;
      if (j >= n - i - 1) {
        j = 0;
        i++;
        setSortedCount(i);
        stateRef.current.swapped = false;
      }

      stateRef.current = { i, j, swapped: stateRef.current.swapped, arr };
    }, 350);
  };

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        stepBubbleSort();
      }, 900);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying]);

  return (
    <div className="bg-theme-surface border border-theme-border rounded-xl p-6 shadow-xl w-full max-w-3xl mx-auto flex flex-col md:flex-row gap-6">
      {/* Visualizer Canvas Area */}
      <div className="flex-1 flex flex-col justify-between">
        <div>
          <h4 className="font-display font-bold text-lg text-theme-accent mb-1">Sorting steps simulator</h4>
          <p className="text-xs text-theme-subtle mb-4">Observe how memory operations map to code lines in real-time.</p>
        </div>
        <div className="h-44 flex items-end gap-3 px-2 border-b border-theme-border pb-2 justify-center">
          {array.map((val, idx) => {
            const isComparing = activeIndices.includes(idx);
            const isSorted = idx >= array.length - sortedCount;
            let barColor = 'bg-theme-subtle opacity-60';
            if (isComparing) barColor = 'bg-theme-accent animate-pulse';
            else if (isSorted) barColor = 'bg-emerald-500 opacity-90';
            
            return (
              <div key={idx} className="flex flex-col items-center flex-1 transition-all duration-300">
                <span className="text-xs mb-1 font-mono text-theme-text">{val}</span>
                <div 
                  className={`w-full rounded-t-sm transition-all duration-300 ${barColor}`}
                  style={{ height: `${val * 1.3}px` }}
                />
              </div>
            );
          })}
        </div>
        
        {/* Visualizer Controls */}
        <div className="flex gap-4 mt-6 justify-center">
          <button 
            id="btn-play-viz"
            onClick={() => setIsPlaying(!isPlaying)} 
            className="flex items-center gap-2 bg-theme-accent hover:opacity-90 text-white font-semibold px-4 py-2 rounded-lg transition-all shadow-md active:scale-95"
          >
            {isPlaying ? <FaPause size={12} /> : <FaPlay size={12} />}
            <span>{isPlaying ? 'Pause' : 'Auto Play'}</span>
          </button>
          <button 
            id="btn-step-viz"
            onClick={stepBubbleSort} 
            disabled={isPlaying}
            className="flex items-center gap-2 border border-theme-border hover:bg-theme-border text-theme-text font-semibold px-4 py-2 rounded-lg disabled:opacity-40 transition-all active:scale-95"
          >
            <FaStepForward size={12} />
            <span>Step</span>
          </button>
          <button 
            id="btn-reset-viz"
            onClick={resetVisualizer}
            className="flex items-center gap-2 border border-theme-border hover:bg-theme-border text-theme-text font-semibold px-4 py-2 rounded-lg transition-all active:scale-95"
          >
            <FaUndo size={12} />
            <span>Reset</span>
          </button>
        </div>
      </div>

      {/* Python Code Trace Area */}
      <div className="w-full md:w-64 bg-theme-bg border border-theme-border rounded-lg p-4 font-mono text-xs select-none">
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
                className={`py-1 px-2 rounded whitespace-pre transition-all duration-200 ${
                  isHighlighted 
                    ? 'bg-theme-accent bg-opacity-20 text-theme-accent font-bold border-l-2 border-theme-accent shadow-sm' 
                    : 'text-theme-text opacity-50'
                }`}
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
