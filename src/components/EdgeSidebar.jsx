import React, { useState, useMemo, useRef, useEffect } from 'react';
import { 
  X, 
  Folder, 
  ChevronRight, 
  ChevronDown, 
  FileText, 
  Search,
  HardDrive,
  FoldVertical,
  UnfoldVertical
} from 'lucide-react';

export default function EdgeSidebar({
  isOpen,
  onClose,
  subjects = [],
  activeDeckId,
  onSelectDeck
}) {
  const [searchFilter, setSearchFilter] = useState('');
  const scrollContainerRef = useRef(null);

  // Restore folder expanded states from sessionStorage (isolated per browser tab)
  const [expandedCategories, setExpandedCategories] = useState(() => {
    try {
      const saved = sessionStorage.getItem('study_menu_expanded_folders');
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error('Error parsing stored folder states', e);
    }
    return {};
  });

  // Restore subject expanded states from sessionStorage (isolated per browser tab)
  const [expandedSubjects, setExpandedSubjects] = useState(() => {
    try {
      const saved = sessionStorage.getItem('study_menu_expanded_subjects');
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error('Error parsing stored subject states', e);
    }
    return {};
  });

  // Restore sidebar scroll position on mount
  useEffect(() => {
    try {
      const savedScroll = sessionStorage.getItem('study_sidebar_scroll_top');
      if (savedScroll && scrollContainerRef.current) {
        scrollContainerRef.current.scrollTop = parseInt(savedScroll, 10);
      }
    } catch (e) {}
  }, []);

  const handleSidebarScroll = (e) => {
    try {
      sessionStorage.setItem('study_sidebar_scroll_top', String(e.currentTarget.scrollTop));
    } catch (err) {}
  };

  const saveExpandedState = (state) => {
    try {
      sessionStorage.setItem('study_menu_expanded_folders', JSON.stringify(state));
    } catch (e) {
      console.error('Error saving folder states', e);
    }
  };

  const saveExpandedSubjects = (state) => {
    try {
      sessionStorage.setItem('study_menu_expanded_subjects', JSON.stringify(state));
    } catch (e) {
      console.error('Error saving subject states', e);
    }
  };

  // Instant single-click toggle for subject
  const toggleSubject = (subjectCode) => {
    setExpandedSubjects(prev => {
      const isCurrentlyOpen = prev[subjectCode] ?? true;
      const next = {
        ...prev,
        [subjectCode]: !isCurrentlyOpen
      };
      saveExpandedSubjects(next);
      return next;
    });
  };

  // Instant single-click toggle for category folder
  const toggleCategory = (catKey) => {
    setExpandedCategories(prev => {
      const isCurrentlyOpen = prev[catKey] ?? true;
      const next = {
        ...prev,
        [catKey]: !isCurrentlyOpen
      };
      saveExpandedState(next);
      return next;
    });
  };

  // Collect all category keys across all subjects
  const allCategoryKeys = useMemo(() => {
    const keys = [];
    (subjects || []).forEach(s => {
      (s.decks || []).forEach(d => {
        const cat = d.category || 'General';
        const key = `${s.code}_${cat}`;
        if (!keys.includes(key)) {
          keys.push(key);
        }
      });
    });
    return keys;
  }, [subjects]);

  // Collapse all subjects & folders at once
  const handleCollapseAll = () => {
    const nextCats = {};
    allCategoryKeys.forEach(k => {
      nextCats[k] = false;
    });
    setExpandedCategories(nextCats);
    saveExpandedState(nextCats);

    const nextSubs = {};
    (subjects || []).forEach(s => {
      nextSubs[s.code] = false;
    });
    setExpandedSubjects(nextSubs);
    saveExpandedSubjects(nextSubs);
  };

  // Expand all subjects & folders at once
  const handleExpandAll = () => {
    const nextCats = {};
    allCategoryKeys.forEach(k => {
      nextCats[k] = true;
    });
    setExpandedCategories(nextCats);
    saveExpandedState(nextCats);

    const nextSubs = {};
    (subjects || []).forEach(s => {
      nextSubs[s.code] = true;
    });
    setExpandedSubjects(nextSubs);
    saveExpandedSubjects(nextSubs);
  };

  // Filter decks by query if typed
  const filteredSubjects = useMemo(() => {
    const q = searchFilter.trim().toLowerCase();
    if (!q) return subjects;

    return subjects.map(s => {
      const matchedDecks = s.decks.filter(d => 
        d.title.toLowerCase().includes(q) ||
        d.category.toLowerCase().includes(q) ||
        s.shortName.toLowerCase().includes(q)
      );
      return { ...s, decks: matchedDecks };
    }).filter(s => s.decks.length > 0);
  }, [subjects, searchFilter]);

  const totalFiles = useMemo(() => {
    return filteredSubjects.reduce((acc, s) => acc + s.decks.length, 0);
  }, [filteredSubjects]);

  return (
    <>
      {/* Backdrop overlay for clicking outside */}
      <div 
        className={`fixed inset-0 bg-black/60 z-40 backdrop-blur-[1px] transition-opacity duration-200 ${
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Edge PDF Left Sidebar Drawer */}
      <aside 
        className={`fixed top-0 bottom-0 left-0 w-80 max-w-[85vw] bg-[#252526] text-slate-200 border-r border-[#3c4043] z-50 flex flex-col shadow-2xl font-sans select-none transition-transform duration-250 ease-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        aria-label="5th Sem Files Navigation"
      >
        {/* Header */}
        <div className="h-12 border-b border-[#3c4043] px-3 flex items-center justify-between shrink-0 bg-[#2d2d2d]">
          <div className="flex items-center space-x-2">
            <HardDrive className="w-4 h-4 text-sky-400 shrink-0" />
            <div className="flex items-center space-x-1.5">
              <span className="text-xs font-semibold text-white tracking-wide">
                5th Sem Files
              </span>
              <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-[#3a3a3a] text-slate-300 font-mono">
                {totalFiles}
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded text-slate-400 hover:text-white hover:bg-[#3e3e3e] transition-colors cursor-pointer"
            title="Close menu (Esc)"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Quick Search in Files */}
        <div className="p-2 border-b border-[#333] bg-[#1e1e1e]">
          <div className="relative flex items-center">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 pointer-events-none" />
            <input
              type="text"
              placeholder="Search 5th Sem files..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              className="w-full bg-[#2a2a2a] border border-[#444] rounded px-2.5 py-1 pl-8 pr-7 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
            />
            {searchFilter && (
              <button
                type="button"
                onClick={() => setSearchFilter('')}
                className="absolute right-2 text-slate-400 hover:text-white text-xs p-0.5"
                title="Clear search"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Quick Expand / Collapse Folders Bar */}
        <div className="px-3 py-1.5 border-b border-[#333] bg-[#222] flex items-center justify-between text-[11px] text-slate-400 shrink-0 select-none">
          <span className="font-medium text-slate-400 text-[10px] uppercase tracking-wider">
            Folders ({allCategoryKeys.length})
          </span>
          <div className="flex items-center space-x-2">
            <button
              type="button"
              onClick={handleExpandAll}
              className="hover:text-sky-400 transition-colors flex items-center space-x-1 cursor-pointer"
              title="Expand all folders"
            >
              <UnfoldVertical className="w-3 h-3 text-sky-400" />
              <span>Expand All</span>
            </button>
            <span className="text-slate-600">|</span>
            <button
              type="button"
              onClick={handleCollapseAll}
              className="hover:text-amber-400 transition-colors flex items-center space-x-1 cursor-pointer"
              title="Collapse all folders"
            >
              <FoldVertical className="w-3 h-3 text-amber-400" />
              <span>Collapse All</span>
            </button>
          </div>
        </div>

        {/* File Navigation Tree */}
        <div 
          ref={scrollContainerRef}
          onScroll={handleSidebarScroll}
          className="flex-1 overflow-y-auto p-2 space-y-3"
        >
          {filteredSubjects.map(subject => {
            // Group decks by category
            const categories = subject.decks.reduce((acc, deck) => {
              const cat = deck.category || 'General';
              if (!acc[cat]) acc[cat] = [];
              acc[cat].push(deck);
              return acc;
            }, {});

            const isSubjectExpanded = searchFilter.trim()
              ? true 
              : (expandedSubjects[subject.code] ?? true);

            return (
              <div key={subject.code} className="space-y-1">
                {/* Collapsible Subject Title */}
                <button
                  type="button"
                  onClick={() => toggleSubject(subject.code)}
                  className="w-full flex items-center justify-between px-2 py-1.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-[#333] rounded transition-colors cursor-pointer group"
                  title={`${subject.shortName} (${subject.decks.length} files) - Click to ${isSubjectExpanded ? 'collapse' : 'expand'}`}
                >
                  <div className="flex items-center space-x-2 truncate">
                    <span 
                      className="w-2.5 h-2.5 rounded-full shrink-0 shadow-sm" 
                      style={{ backgroundColor: subject.color || '#38bdf8' }} 
                    />
                    <span className="truncate tracking-wide text-slate-200 group-hover:text-white font-bold">
                      {subject.shortName}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono font-normal">
                      ({subject.decks.length})
                    </span>
                  </div>
                  <div className="flex items-center space-x-1 shrink-0 text-slate-400 group-hover:text-slate-200 transition-colors">
                    {isSubjectExpanded ? (
                      <ChevronDown className="w-3.5 h-3.5" />
                    ) : (
                      <ChevronRight className="w-3.5 h-3.5" />
                    )}
                  </div>
                </button>

                {/* Categories */}
                {isSubjectExpanded && (
                  <div className="space-y-1 pl-2 border-l border-[#333]/60 ml-2">
                    {Object.entries(categories).map(([categoryName, decks]) => {
                      const catKey = `${subject.code}_${categoryName}`;
                      const isExpanded = searchFilter.trim()
                        ? true 
                        : (expandedCategories[catKey] ?? true);

                      return (
                        <div key={categoryName} className="space-y-0.5">
                          <button
                            type="button"
                            onClick={() => toggleCategory(catKey)}
                            className="w-full flex items-center justify-between px-2 py-1.5 text-[11px] font-medium text-slate-400 hover:text-white hover:bg-[#333] rounded group cursor-pointer transition-colors"
                            title={`${categoryName} (${decks.length} files) - Click to ${isExpanded ? 'collapse' : 'expand'}`}
                          >
                            <div className="flex items-center space-x-1.5 truncate">
                              <Folder className="w-3.5 h-3.5 text-slate-500 group-hover:text-sky-400 shrink-0 transition-colors" />
                              <span className="truncate">{categoryName}</span>
                            </div>
                            <div className="flex items-center space-x-1.5 shrink-0">
                              <span className="text-[10px] text-slate-500 font-mono">
                                {decks.length}
                              </span>
                              {isExpanded ? (
                                <ChevronDown className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300 transition-transform" />
                              ) : (
                                <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300 transition-transform" />
                              )}
                            </div>
                          </button>

                          {/* File Items */}
                          {isExpanded && (
                            <div className="space-y-0.5 pl-3 border-l border-[#3a3a3a] ml-2">
                              {decks.map(deck => {
                                const isActive = activeDeckId === deck.id;
                                const isPpt = deck.fileType?.includes('PPT');

                                return (
                                  <button
                                    key={deck.id}
                                    type="button"
                                    onClick={() => {
                                      onSelectDeck(deck.id);
                                      onClose();
                                    }}
                                    className={`w-full text-left px-2 py-1.5 rounded text-xs transition-colors flex items-center justify-between group cursor-pointer ${
                                      isActive
                                        ? 'bg-sky-600/30 text-white font-medium border border-sky-500/50'
                                        : 'text-slate-300 hover:text-white hover:bg-[#333]'
                                    }`}
                                    title={`${deck.title} (${deck.slideCount} pages)`}
                                  >
                                    <div className="truncate pr-2">
                                      <div className="truncate text-[12px] group-hover:text-white">
                                        {deck.title}
                                      </div>
                                      <div className="text-[10px] text-slate-500 font-mono">
                                        {deck.slideCount} pages
                                      </div>
                                    </div>
                                    <span className={`text-[9px] px-1 py-0.2 rounded font-mono font-semibold shrink-0 ${
                                      isPpt 
                                        ? 'bg-amber-950/60 text-amber-400 border border-amber-600/30' 
                                        : 'bg-rose-950/60 text-rose-400 border border-rose-600/30'
                                    }`}>
                                      {deck.fileType}
                                    </span>
                                  </button>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer info */}
        <div className="p-3 border-t border-[#3c4043] bg-[#222] text-[11px] text-slate-400">
          <p className="truncate text-slate-300 font-medium">SFIT 5th Sem Studies</p>
          <p className="text-[10px] text-slate-500 truncate mt-0.5">
            C:\Users\kevin\Studies\SFIT\5th Sem
          </p>
        </div>
      </aside>
    </>
  );
}
