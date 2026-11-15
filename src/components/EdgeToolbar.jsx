import React, { useState, useEffect, useRef } from 'react';
import { 
  Menu, 
  Minus, 
  Plus, 
  MoveHorizontal, 
  RotateCw, 
  Pin, 
  PinOff,
  Search,
  Type
} from 'lucide-react';

export default function EdgeToolbar({
  documentTitle,
  fileType,
  currentPage,
  totalPages,
  onPageJump,
  zoom,
  onZoomChange,
  onFitWidth,
  rotation,
  onRotate,
  isSidebarOpen,
  onToggleSidebar,
  isPinned,
  onTogglePinned,
  isToolbarVisible,
  onOpenSearch,
  onMouseEnter,
  onMouseLeave
}) {
  const [inputVal, setInputVal] = useState(currentPage.toString());
  const toolbarRef = useRef(null);

  useEffect(() => {
    setInputVal(currentPage.toString());
  }, [currentPage]);

  // Keep toolbar pinned to physical screen top during native browser pinch-zoom
  useEffect(() => {
    if (!window.visualViewport) return;
    const handleViewport = () => {
      const vv = window.visualViewport;
      const el = toolbarRef.current;
      if (!el) return;
      if (vv.scale > 1.01) {
        const yOffset = isToolbarVisible ? vv.offsetTop : vv.offsetTop - (48 * vv.scale);
        el.style.transform = `translate(${vv.offsetLeft}px, ${yOffset}px) scale(${1 / vv.scale})`;
        el.style.transformOrigin = 'top left';
        el.style.width = `${vv.width * vv.scale}px`;
      } else {
        // Clear inline overrides so CSS transition classes control visibility smoothly
        el.style.transform = '';
        el.style.transformOrigin = '';
        el.style.width = '';
      }
    };

    handleViewport();
    window.visualViewport.addEventListener('resize', handleViewport);
    window.visualViewport.addEventListener('scroll', handleViewport);
    return () => {
      window.visualViewport.removeEventListener('resize', handleViewport);
      window.visualViewport.removeEventListener('scroll', handleViewport);
    };
  }, [isToolbarVisible]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsed = parseInt(inputVal, 10);
    if (!isNaN(parsed) && parsed >= 1 && parsed <= totalPages) {
      onPageJump(parsed);
    } else {
      setInputVal(currentPage.toString());
    }
  };

  return (
    <div 
      ref={toolbarRef}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      className={`fixed top-0 left-0 right-0 h-12 bg-[#2b2b2b] text-slate-200 border-b border-[#3c4043] px-3 flex items-center justify-between z-40 shadow-md transition-all duration-200 ease-in-out select-none ${
        isToolbarVisible ? 'translate-y-0 opacity-100 pointer-events-auto' : '-translate-y-full opacity-0 pointer-events-none'
      }`}
    >
      {/* Left Section: Menu Toggle, Document Title, Page Input */}
      <div className="flex items-center space-x-2 min-w-0">
        {/* Expandable Left Menu / 5th Sem Files Button */}
        <button
          onClick={onToggleSidebar}
          className={`p-1.5 rounded transition-colors flex items-center justify-center ${
            isSidebarOpen 
              ? 'bg-[#404040] text-sky-400' 
              : 'text-slate-300 hover:bg-[#383838] hover:text-white'
          }`}
          title="Contents / 5th Sem Files (Click to expand menu)"
          aria-label="Expand 5th Sem Files Menu"
        >
          <Menu className="w-4 h-4" />
        </button>

        <div className="w-[1px] h-4 bg-[#4a4a4a]" />

        {/* Document Title */}
        <div className="min-w-0 flex items-center space-x-2">
          <span 
            className="text-xs font-medium text-slate-100 truncate max-w-[200px] sm:max-w-[320px]" 
            title={documentTitle}
          >
            {documentTitle}
          </span>
          <span className="text-[10px] px-1 py-0.2 rounded bg-[#383838] text-slate-400 font-mono">
            {fileType}
          </span>
        </div>

        <div className="w-[1px] h-4 bg-[#4a4a4a]" />

        {/* Edge Style Page Counter Input: [ 6 ] / 70 */}
        <form onSubmit={handleSubmit} className="flex items-center space-x-1 text-xs">
          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onBlur={handleSubmit}
            className="w-10 text-center bg-[#1e1e1e] border border-[#555] rounded py-0.5 text-xs text-white font-mono focus:outline-none focus:border-sky-500"
            title="Type page number and press Enter"
          />
          <span className="text-slate-400 font-mono text-xs">/ {totalPages}</span>
        </form>
      </div>

      {/* Right Section: Zoom, Fit Width, Rotate, Text Cursor, Pin */}
      <div className="flex items-center space-x-1 text-xs">
        {/* Zoom Out */}
        <button
          onClick={() => onZoomChange(Math.max(40, zoom - 15))}
          className="p-1.5 rounded text-slate-300 hover:bg-[#383838] hover:text-white transition-colors"
          title="Zoom out"
        >
          <Minus className="w-4 h-4" />
        </button>

        {/* Zoom Percentage */}
        <button
          onClick={() => onZoomChange(100)}
          className="px-2 py-0.5 rounded text-xs font-mono text-slate-200 hover:bg-[#383838] hover:text-white transition-colors min-w-[3.5rem] text-center"
          title="Reset zoom to 100%"
        >
          {zoom}%
        </button>

        {/* Zoom In */}
        <button
          onClick={() => onZoomChange(Math.min(300, zoom + 15))}
          className="p-1.5 rounded text-slate-300 hover:bg-[#383838] hover:text-white transition-colors"
          title="Zoom in"
        >
          <Plus className="w-4 h-4" />
        </button>

        <div className="w-[1px] h-4 bg-[#4a4a4a] mx-1" />

        {/* Fit to Width */}
        <button
          onClick={onFitWidth}
          className="p-1.5 rounded text-slate-300 hover:bg-[#383838] hover:text-white transition-colors"
          title="Fit to width"
        >
          <MoveHorizontal className="w-4 h-4" />
        </button>

        {/* Rotate Clockwise */}
        <button
          onClick={onRotate}
          className="p-1.5 rounded text-slate-300 hover:bg-[#383838] hover:text-white transition-colors"
          title="Rotate clockwise"
        >
          <RotateCw className="w-4 h-4" />
        </button>

        <div className="w-[1px] h-4 bg-[#4a4a4a] mx-1" />

        {/* Text Selection indicator */}
        <div 
          className="p-1.5 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30"
          title="Text selection enabled (click & drag to select)"
        >
          <Type className="w-4 h-4" />
        </div>

        {/* Search */}
        <button
          onClick={onOpenSearch}
          className="p-1.5 rounded text-slate-300 hover:bg-[#383838] hover:text-white transition-colors"
          title="Find in document (Ctrl + F)"
        >
          <Search className="w-4 h-4" />
        </button>

        <div className="w-[1px] h-4 bg-[#4a4a4a] mx-1" />

        {/* Pin / Unpin Top Bar (Edge Style) */}
        <button
          onClick={onTogglePinned}
          className={`p-1.5 rounded transition-colors ${
            isPinned 
              ? 'text-sky-400 bg-sky-500/20 border border-sky-500/30' 
              : 'text-slate-400 hover:bg-[#383838] hover:text-white'
          }`}
          title={isPinned ? "Unpin toolbar (Auto-hide on scroll)" : "Pin toolbar to stay visible"}
        >
          {isPinned ? <Pin className="w-4 h-4" /> : <PinOff className="w-4 h-4" />}
        </button>
      </div>
    </div>
  );
}
