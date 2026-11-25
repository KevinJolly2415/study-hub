import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import EdgeToolbar from './components/EdgeToolbar';
import EdgeSidebar from './components/EdgeSidebar';
import EdgeDocumentViewer from './components/EdgeDocumentViewer';
import EdgeFindBar from './components/EdgeFindBar';
import { Loader2, AlertCircle, RefreshCw, Menu } from 'lucide-react';

// Clean up legacy cross-tab scroll positions from localStorage once
try {
  Object.keys(localStorage).forEach(k => {
    if (k.startsWith('study_deck_pos_')) {
      localStorage.removeItem(k);
    }
  });
} catch (e) {}

export default function App() {
  const [manifest, setManifest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active document / deck (isolated per tab via URL param and sessionStorage)
  const [activeDeckId, setActiveDeckId] = useState(() => {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const urlDeck = urlParams.get('deck');
      if (urlDeck) return urlDeck;
      return sessionStorage.getItem('study_last_deck_id') || localStorage.getItem('study_last_deck_id') || null;
    } catch (e) {
      return null;
    }
  });

  // Current page number (restored per document and strictly isolated per tab)
  const [currentPage, setCurrentPage] = useState(() => {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const urlPage = parseInt(urlParams.get('page'), 10);
      if (!isNaN(urlPage) && urlPage >= 1) return urlPage;

      const savedDeckId = urlParams.get('deck') || sessionStorage.getItem('study_last_deck_id') || localStorage.getItem('study_last_deck_id');
      if (savedDeckId) {
        const perDeck = sessionStorage.getItem(`study_deck_pos_${savedDeckId}`);
        if (perDeck) return parseInt(perDeck, 10);
      }
    } catch (e) {}
    return 1;
  });

  // Zoom level (default 100%, isolated per tab in sessionStorage)
  const [zoom, setZoom] = useState(() => {
    const saved = sessionStorage.getItem('study_edge_zoom');
    return saved ? parseInt(saved, 10) : 100;
  });

  // Rotation (0, 90, 180, 270, isolated per tab in sessionStorage)
  const [rotation, setRotation] = useState(() => {
    const saved = sessionStorage.getItem('study_edge_rotation');
    return saved ? parseInt(saved, 10) : 0;
  });

  // Expandable left sidebar (saved per tab in sessionStorage)
  const [isSidebarOpen, setIsSidebarOpen] = useState(() => {
    try {
      const saved = sessionStorage.getItem('study_sidebar_open');
      return saved !== null ? saved === 'true' : false;
    } catch (e) {
      return false;
    }
  });

  // Topbar pinned state (like MS Edge PDF viewer)
  const [isPinned, setIsPinned] = useState(() => {
    const saved = localStorage.getItem('study_edge_pinned');
    return saved !== null ? saved === 'true' : true; // Default pinned
  });

  // Auto-hide toolbar visibility when unpinned
  const [isMouseNearTop, setIsMouseNearTop] = useState(false);
  const [isToolbarHovered, setIsToolbarHovered] = useState(false);
  const hideTimerRef = useRef(null);

  // Reliable window-level mouse movement tracker for top hover zone
  useEffect(() => {
    if (isPinned) {
      setIsMouseNearTop(false);
      return;
    }

    const handleWindowMouseMove = (e) => {
      // Top 75px zone triggers toolbar reveal
      if (e.clientY <= 75) {
        if (hideTimerRef.current) {
          clearTimeout(hideTimerRef.current);
          hideTimerRef.current = null;
        }
        setIsMouseNearTop(true);
      } else if (!isToolbarHovered) {
        // Generous grace period of 1.2s so the toolbar never disappears abruptly
        if (!hideTimerRef.current) {
          hideTimerRef.current = setTimeout(() => {
            setIsMouseNearTop(false);
            hideTimerRef.current = null;
          }, 1200);
        }
      }
    };

    window.addEventListener('mousemove', handleWindowMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleWindowMouseMove);
      if (hideTimerRef.current) clearTimeout(hideTimerRef.current);
    };
  }, [isPinned, isToolbarHovered]);

  // Ctrl + F Find Bar
  const [isFindBarOpen, setIsFindBarOpen] = useState(false);
  const [findQuery, setFindQuery] = useState('');
  const [currentMatchIndex, setCurrentMatchIndex] = useState(0);

  // Load Manifest
  const loadManifest = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/data/manifest.json?t=' + Date.now());
      if (!res.ok) {
        throw new Error(`Failed to load manifest (${res.status})`);
      }
      const data = await res.json();
      setManifest(data);

      const allDecks = (data.subjects || []).flatMap(s => s.decks);
      if (allDecks.length > 0) {
        setActiveDeckId(prev => {
          if (prev && allDecks.some(d => d.id === prev)) {
            return prev;
          }
          return allDecks[0].id;
        });
      }
    } catch (err) {
      console.error("Manifest load error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadManifest();
  }, [loadManifest]);

  // Persist State (strictly isolated per tab via sessionStorage & URL query)
  useEffect(() => {
    if (activeDeckId) {
      try {
        sessionStorage.setItem('study_last_deck_id', activeDeckId);
        sessionStorage.setItem(`study_deck_pos_${activeDeckId}`, currentPage.toString());
        // Update URL query parameters so copying/opening links or refreshing stays on the exact deck and page
        const url = new URL(window.location.href);
        url.searchParams.set('deck', activeDeckId);
        url.searchParams.set('page', currentPage.toString());
        window.history.replaceState(null, '', url.toString());
      } catch (e) {}
    }
  }, [activeDeckId, currentPage]);

  useEffect(() => {
    try {
      sessionStorage.setItem('study_edge_zoom', zoom.toString());
    } catch (e) {}
  }, [zoom]);

  useEffect(() => {
    try {
      sessionStorage.setItem('study_sidebar_open', String(isSidebarOpen));
    } catch (e) {}
  }, [isSidebarOpen]);

  useEffect(() => {
    localStorage.setItem('study_edge_pinned', isPinned.toString());
  }, [isPinned]);

  useEffect(() => {
    try {
      sessionStorage.setItem('study_edge_rotation', rotation.toString());
    } catch (e) {}
  }, [rotation]);

  // Derived current deck & subject
  const { currentSubject, currentDeck } = useMemo(() => {
    if (!manifest || !manifest.subjects) return { currentSubject: null, currentDeck: null };

    for (const sub of manifest.subjects) {
      const deck = sub.decks.find(d => d.id === activeDeckId);
      if (deck) {
        return { currentSubject: sub, currentDeck: deck };
      }
    }
    return { currentSubject: null, currentDeck: null };
  }, [manifest, activeDeckId]);

  // Switch to another file from the expandable menu (isolated per tab)
  const handleSelectDeck = (deckId) => {
    setActiveDeckId(deckId);
    const saved = sessionStorage.getItem(`study_deck_pos_${deckId}`);
    setCurrentPage(saved ? parseInt(saved, 10) : 1);
  };

  // Jump to page (from [ 6 ] input, isolated per tab)
  const handlePageJump = (pageNum) => {
    if (!currentDeck) return;
    const clamped = Math.max(1, Math.min(pageNum, currentDeck.slides.length));
    setCurrentPage(clamped);

    const el = document.getElementById(`page-${clamped}`);
    if (el) {
      el.scrollIntoView({ behavior: 'auto', block: 'start' });
    }
    if (activeDeckId) {
      sessionStorage.setItem(`study_deck_pos_${activeDeckId}`, clamped.toString());
    }
  };

  // Page updated on scroll (strictly updates only this tab's state & sessionStorage)
  const handlePageChange = (pageNum) => {
    setCurrentPage(pageNum);
    if (activeDeckId) {
      sessionStorage.setItem(`study_deck_pos_${activeDeckId}`, pageNum.toString());
    }
  };

  // Fit to Width handler
  const handleFitWidth = () => {
    // Fits slide to approximately 94% of window width
    const targetWidth = window.innerWidth * 0.92;
    const computedZoom = Math.round((targetWidth / 850) * 100);
    setZoom(Math.min(250, Math.max(50, computedZoom)));
  };

  // Rotate handler (cycles 0 -> 90 -> 180 -> 270)
  const handleRotate = () => {
    setRotation(prev => (prev + 90) % 360);
  };

  // Browser back/forward navigation support
  useEffect(() => {
    const handlePopState = () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const urlDeck = urlParams.get('deck');
        const urlPage = parseInt(urlParams.get('page'), 10);
        if (urlDeck) {
          setActiveDeckId(urlDeck);
        }
        if (!isNaN(urlPage) && urlPage >= 1) {
          setCurrentPage(urlPage);
          const el = document.getElementById(`page-${urlPage}`);
          if (el) el.scrollIntoView({ behavior: 'auto', block: 'start' });
        }
      } catch (e) {}
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Keyboard Shortcuts (Ctrl+F, Ctrl+B, Esc)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'f') {
        e.preventDefault();
        setIsFindBarOpen(true);
        return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault();
        setIsSidebarOpen(prev => !prev);
        return;
      }
      if (e.key === 'Escape') {
        if (isFindBarOpen) {
          setIsFindBarOpen(false);
          return;
        }
        if (isSidebarOpen) {
          setIsSidebarOpen(false);
          return;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isFindBarOpen, isSidebarOpen]);

  // Find in Document Matches
  const searchMatches = useMemo(() => {
    const q = findQuery.trim().toLowerCase();
    if (!q || !currentDeck) return [];

    const matches = [];
    currentDeck.slides.forEach((slide) => {
      if (slide.text && slide.text.toLowerCase().includes(q)) {
        matches.push(slide.index);
      }
    });
    return matches;
  }, [findQuery, currentDeck]);

  const handleNextMatch = () => {
    if (searchMatches.length === 0) return;
    const nextIdx = (currentMatchIndex + 1) % searchMatches.length;
    setCurrentMatchIndex(nextIdx);
    handlePageJump(searchMatches[nextIdx]);
  };

  const handlePrevMatch = () => {
    if (searchMatches.length === 0) return;
    const prevIdx = (currentMatchIndex - 1 + searchMatches.length) % searchMatches.length;
    setCurrentMatchIndex(prevIdx);
    handlePageJump(searchMatches[prevIdx]);
  };

  if (loading) {
    return (
      <div className="h-screen w-screen flex flex-col items-center justify-center bg-[#1b1b1b] text-slate-200">
        <Loader2 className="w-8 h-8 text-sky-500 animate-spin mb-3" />
        <h2 className="text-sm font-medium">Loading SFIT 5th Sem Documents...</h2>
      </div>
    );
  }

  if (error || !manifest) {
    return (
      <div className="h-screen w-screen flex flex-col items-center justify-center bg-[#1b1b1b] text-slate-200 p-6 text-center">
        <AlertCircle className="w-10 h-10 text-rose-500 mb-3" />
        <h2 className="text-base font-medium mb-2">Could Not Load Documents</h2>
        <button
          onClick={loadManifest}
          className="flex items-center space-x-2 px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry</span>
        </button>
      </div>
    );
  }

  const isToolbarVisible = isPinned || isMouseNearTop || isToolbarHovered || isFindBarOpen || isSidebarOpen;

  return (
    <div className="h-screen w-screen flex flex-col bg-[#1b1b1b] overflow-hidden font-sans select-none relative">
      {/* Invisible top hover trigger strip */}
      {!isPinned && !isToolbarVisible && (
        <div 
          className="fixed top-0 left-0 right-0 h-4 z-50 pointer-events-auto"
          onMouseEnter={() => {
            if (hideTimerRef.current) clearTimeout(hideTimerRef.current);
            setIsMouseNearTop(true);
          }}
        />
      )}

      {/* Microsoft Edge PDF Toolbar (Replica) */}
      <EdgeToolbar
        documentTitle={currentDeck?.title || 'Document'}
        fileType={currentDeck?.fileType || 'PDF'}
        currentPage={currentPage}
        totalPages={currentDeck?.slideCount || 1}
        onPageJump={handlePageJump}
        zoom={zoom}
        onZoomChange={setZoom}
        onFitWidth={handleFitWidth}
        rotation={rotation}
        onRotate={handleRotate}
        isSidebarOpen={isSidebarOpen}
        onToggleSidebar={() => setIsSidebarOpen(prev => !prev)}
        isPinned={isPinned}
        onTogglePinned={() => setIsPinned(prev => !prev)}
        isToolbarVisible={isToolbarVisible}
        onOpenSearch={() => setIsFindBarOpen(prev => !prev)}
        onMouseEnter={() => {
          if (hideTimerRef.current) clearTimeout(hideTimerRef.current);
          setIsToolbarHovered(true);
          setIsMouseNearTop(true);
        }}
        onMouseLeave={() => {
          setIsToolbarHovered(false);
          if (!isPinned) {
            hideTimerRef.current = setTimeout(() => {
              setIsMouseNearTop(false);
              hideTimerRef.current = null;
            }, 1200);
          }
        }}
      />

      {/* Expandable Left Menu / 5th Sem Files Drawer */}
      <EdgeSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        subjects={manifest.subjects}
        activeDeckId={activeDeckId}
        onSelectDeck={handleSelectDeck}
      />

      {/* Expandable Menu Tab on Left Edge (Click to expand 5th Sem files) */}
      {!isSidebarOpen && (
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="fixed left-0 top-1/2 -translate-y-1/2 z-30 flex flex-col items-center py-3 px-1.5 bg-[#252526]/90 hover:bg-[#323234] text-slate-300 hover:text-white border-y border-r border-[#444] rounded-r-md shadow-xl transition-all group backdrop-blur-sm cursor-pointer"
          title="Expand 5th Sem Files Menu (Ctrl+B)"
          aria-label="Expand 5th Sem Files Menu"
        >
          <Menu className="w-4 h-4 text-sky-400 group-hover:scale-110 transition-transform mb-1.5" />
          <span className="text-[10px] font-semibold [writing-mode:vertical-rl] tracking-wider text-slate-300 group-hover:text-white uppercase select-none">
            5th Sem Files
          </span>
        </button>
      )}

      {/* Find in Document Bar (Ctrl + F) */}
      <EdgeFindBar
        isOpen={isFindBarOpen}
        onClose={() => setIsFindBarOpen(false)}
        query={findQuery}
        onQueryChange={(q) => {
          setFindQuery(q);
          setCurrentMatchIndex(0);
        }}
        matchesCount={searchMatches.length}
        currentMatch={currentMatchIndex}
        onNextMatch={handleNextMatch}
        onPrevMatch={handlePrevMatch}
      />

      {/* Main Document Canvas: Smooth Continuous Scroll + Trackpad Pinch-to-Zoom */}
      <main className="flex-1 w-full h-full relative overflow-hidden">
        <EdgeDocumentViewer
          deck={currentDeck}
          currentPage={currentPage}
          onPageChange={handlePageChange}
          zoom={zoom}
          onZoomChange={setZoom}
          rotation={rotation}
          isPinned={isPinned}
          onMouseMoveTop={setIsMouseNearTop}
        />
      </main>
    </div>
  );
}
