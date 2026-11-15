import React, { useRef, useEffect } from 'react';
import { Search, ChevronUp, ChevronDown, X } from 'lucide-react';

export default function EdgeFindBar({
  isOpen,
  onClose,
  query,
  onQueryChange,
  matchesCount,
  currentMatch,
  onNextMatch,
  onPrevMatch
}) {
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onNextMatch();
  };

  return (
    <div className="fixed top-14 right-4 z-50 bg-[#2b2b2b] text-slate-200 border border-[#444] rounded-lg shadow-2xl p-2 flex items-center space-x-2 animate-fade-in select-none">
      <Search className="w-4 h-4 text-slate-400 shrink-0" />
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <input
          ref={inputRef}
          type="text"
          placeholder="Find in document..."
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          className="w-48 bg-[#1e1e1e] border border-[#555] rounded px-2.5 py-1 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
        />
      </form>

      <span className="text-xs font-mono text-slate-400 min-w-[3.5rem] text-center">
        {query.trim() ? (
          matchesCount > 0 ? (
            `${currentMatch + 1} of ${matchesCount}`
          ) : (
            '0 / 0'
          )
        ) : (
          '--'
        )}
      </span>

      <button
        onClick={onPrevMatch}
        disabled={matchesCount === 0}
        className="p-1 rounded text-slate-300 hover:text-white hover:bg-[#383838] disabled:opacity-30"
        title="Previous (Shift+Enter)"
      >
        <ChevronUp className="w-4 h-4" />
      </button>

      <button
        onClick={onNextMatch}
        disabled={matchesCount === 0}
        className="p-1 rounded text-slate-300 hover:text-white hover:bg-[#383838] disabled:opacity-30"
        title="Next (Enter)"
      >
        <ChevronDown className="w-4 h-4" />
      </button>

      <button
        onClick={onClose}
        className="p-1 rounded text-slate-400 hover:text-white hover:bg-[#383838]"
        title="Close (Esc)"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}

