import React from 'react';
import { 
  Menu, 
  Sun, 
  Moon, 
  ShieldCheck, 
  Scale, 
  Database, 
  Bookmark,
  Share2
} from 'lucide-react';

export default function Navbar({
  onToggleSidebar,
  darkMode,
  onToggleDarkMode,
  onOpenDocuments,
  onOpenBookmarks,
  vectorCount = 0
}) {
  return (
    <header className="sticky top-0 z-30 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
      {/* Tri-color accent bar for Government aesthetic */}
      <div className="h-1 w-full flex">
        <div className="flex-1 bg-[#FF9933]" title="Saffron" />
        <div className="flex-1 bg-white" title="White" />
        <div className="flex-1 bg-[#138808]" title="Green" />
      </div>

      <div className="px-4 sm:px-6 py-2.5 flex items-center justify-between">
        {/* Left: Mobile Toggle & Title */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-1.5 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden"
            title="Toggle Menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg bg-justice-900 text-gold-400 flex items-center justify-center shadow-sm border border-gold-500/30">
              <Scale className="w-5 h-5 text-gold-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white font-serif leading-tight">
                  AI Justice Department Assistant
                </h1>
                <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-justice-100 text-justice-800 dark:bg-justice-950 dark:text-justice-300 border border-justice-200 dark:border-justice-800">
                  Govt. of India Legal RAG
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 hidden sm:block">
                Autonomous Retrieval over Public Acts, Bharatiya Nyaya Sanhita & Constitutional Provisions
              </p>
            </div>
          </div>
        </div>

        {/* Right: Quick Actions & Status */}
        <div className="flex items-center gap-2">
          {/* Vector Status Pill */}
          <div 
            onClick={onOpenDocuments}
            className="cursor-pointer hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-colors"
            title="Click to view loaded legal acts"
          >
            <Database className="w-3.5 h-3.5 text-justice-600 dark:text-justice-400" />
            <span>{vectorCount > 0 ? `${vectorCount} Chunks Indexed` : 'Document Vault'}</span>
          </div>

          {/* Bookmarks Quick Pill */}
          <button
            onClick={onOpenBookmarks}
            className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium text-slate-700 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Saved Provisions"
          >
            <Bookmark className="w-3.5 h-3.5 text-gold-500" />
            <span>Saved</span>
          </button>

          {/* Theme Toggle */}
          <button
            onClick={onToggleDarkMode}
            className="p-2 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
          >
            {darkMode ? <Sun className="w-4 h-4 text-gold-400" /> : <Moon className="w-4 h-4 text-justice-700" />}
          </button>
        </div>
      </div>
    </header>
  );
}
