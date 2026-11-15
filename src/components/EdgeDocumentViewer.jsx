import React, { useState, useEffect, useLayoutEffect, useRef } from 'react';

export default function EdgeDocumentViewer({
  deck,
  currentPage,
  onPageChange,
  zoom,
  onZoomChange,
  rotation,
  isPinned,
  onMouseMoveTop
}) {
  const containerRef = useRef(null);
  const slideRefs = useRef({});
  const isProgrammaticScrollRef = useRef(false);
  const isRestoredRef = useRef(false);

  const slides = deck?.slides || [];
  const total = slides.length;
  const prevZoomRef = useRef(zoom);

  // Adjust scroll position for discrete toolbar button clicks (+ / - / Fit Width)
  useLayoutEffect(() => {
    const oldZoom = prevZoomRef.current;
    if (oldZoom !== zoom && containerRef.current && oldZoom > 0) {
      if (!isProgrammaticScrollRef.current) {
        const container = containerRef.current;
        const ratio = zoom / oldZoom;
        const viewportH = container.clientHeight;
        const currentCenter = container.scrollTop + viewportH / 2;
        const targetCenter = currentCenter * ratio;
        container.scrollTop = Math.max(0, targetCenter - viewportH / 2);
      }
    }
    prevZoomRef.current = zoom;
  }, [zoom]);

  // Keyboard Zoom Shortcuts (Ctrl + / Ctrl - / Ctrl 0)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === '=' || e.key === '+') {
          e.preventDefault();
          onZoomChange(prev => Math.min(300, prev + 15));
        } else if (e.key === '-' || e.key === '_') {
          e.preventDefault();
          onZoomChange(prev => Math.max(40, prev - 15));
        } else if (e.key === '0') {
          e.preventDefault();
          onZoomChange(100);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onZoomChange]);

  // Restore scroll position to currentPage on deck switch or initial mount
  useEffect(() => {
    isRestoredRef.current = false;
    isProgrammaticScrollRef.current = true;
    const target = currentPage || 1;

    const timer = setTimeout(() => {
      const el = slideRefs.current[target];
      if (el && containerRef.current) {
        el.scrollIntoView({ behavior: 'auto', block: 'start' });
      }
      setTimeout(() => {
        isRestoredRef.current = true;
        isProgrammaticScrollRef.current = false;
      }, 150);
    }, 60);

    return () => clearTimeout(timer);
  }, [deck?.id]);

  // Passive non-blocking scroll listener to update page counter silently
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let ticking = false;

    const handleScroll = () => {
      if (!isRestoredRef.current || isProgrammaticScrollRef.current) return;

      if (!ticking) {
        ticking = true;
        requestAnimationFrame(() => {
          ticking = false;
          if (!container) return;

          const containerTop = container.getBoundingClientRect().top;
          let closestPage = 1;
          let minDiff = Infinity;

          for (let i = 1; i <= total; i++) {
            const el = slideRefs.current[i];
            if (el) {
              const rect = el.getBoundingClientRect();
              const diff = Math.abs(rect.top - containerTop - 40);
              if (diff < minDiff) {
                minDiff = diff;
                closestPage = i;
              }
            }
          }

          if (closestPage !== currentPage) {
            onPageChange(closestPage);
          }
        });
      }
    };

    container.addEventListener('scroll', handleScroll, { passive: true });
    return () => container.removeEventListener('scroll', handleScroll);
  }, [total, currentPage, onPageChange]);

  // Mouse move listener for auto-hide toolbar
  const handleMouseMove = (e) => {
    if (onMouseMoveTop) {
      onMouseMoveTop(e.clientY <= 55);
    }
  };

  // Base width at 100% zoom is 850px
  const slideWidth = Math.round((850 * zoom) / 100);

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      className={`w-full h-full overflow-auto bg-[#1b1b1b] flex flex-col items-center select-text ${
        isPinned ? 'pt-14' : 'pt-4'
      }`}
    >
      <div 
        className="flex flex-col items-center space-y-6 my-4 pb-16"
        style={{ width: `${slideWidth}px` }}
      >
        {slides.map((s) => {
          const slideAspect = s.width && s.height 
            ? s.width / s.height 
            : (deck.aspectRatio || 1.33);

          return (
            <div
              key={s.index}
              ref={(el) => (slideRefs.current[s.index] = el)}
              id={`page-${s.index}`}
              className="relative bg-white shadow-2xl rounded-sm overflow-hidden select-text w-full"
              style={{
                aspectRatio: `${slideAspect}`,
                containerType: 'size',
                transform: rotation ? `rotate(${rotation}deg)` : 'none',
                transition: rotation ? 'transform 0.2s ease-out' : 'none'
              }}
            >
              {/* Rasterized Slide Image */}
              <img
                src={s.image}
                alt={`Page ${s.index}`}
                className="w-full h-full object-contain pointer-events-none select-none block"
                loading="lazy"
              />

              {/* Exact Transparent Text Selection Layer */}
              <div className="absolute inset-0 select-text overflow-hidden z-10 pointer-events-auto">
                {s.rects && s.rects.length > 0 ? (
                  s.rects.map((r, rIdx) => (
                    <span
                      key={rIdx}
                      className="absolute select-text text-transparent cursor-text whitespace-pre leading-none"
                      style={{
                        left: `${r.l}%`,
                        top: `${r.t}%`,
                        width: `${r.w}%`,
                        height: `${r.h}%`,
                        fontSize: `calc(${r.h} * 0.82cqh)`,
                        lineHeight: `calc(${r.h} * 1cqh)`
                      }}
                    >
                      {r.text}
                    </span>
                  ))
                ) : (
                  s.text && (
                    <div className="absolute inset-0 p-8 select-text text-transparent cursor-text opacity-0">
                      {s.text}
                    </div>
                  )
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
