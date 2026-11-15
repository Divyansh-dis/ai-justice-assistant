import React from 'react';
import { 
  Plus, 
  MessageSquare, 
  Trash2, 
  Database, 
  Bookmark, 
  Download, 
  Scale, 
  X,
  ExternalLink
} from 'lucide-react';

export default function Sidebar({
  isOpen,
  onClose,
  sessions,
  currentSessionId,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  onOpenDocuments,
  onOpenBookmarks,
  onOpenExport
}) {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          onClick={onClose}
          className="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-72 bg-slate-900 text-slate-200 border-r border-slate-800 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Header / Brand */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-justice-600 flex items-center justify-center text-white shadow-md">
              <Scale className="w-5 h-5 text-gold-400" />
            </div>
            <div>
              <h2 className="text-sm font-bold tracking-tight text-white font-serif">
                NYAYA ASSISTANT
              </h2>
              <p className="text-[10px] text-slate-400 font-medium tracking-wide">
                GOVT. OF INDIA LEGAL RAG
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 lg:hidden"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action Button: New Legal Inquiry */}
        <div className="p-3">
          <button
            onClick={() => {
              onNewSession();
              if (window.innerWidth < 1024) onClose();
            }}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg bg-justice-600 hover:bg-justice-700 active:bg-justice-800 text-white font-medium text-xs shadow-sm transition-all border border-justice-500/30"
          >
            <Plus className="w-4 h-4" />
            <span>New Legal Inquiry</span>
          </button>
        </div>

        {/* Previous Chat Sessions */}
        <div className="flex-1 overflow-y-auto px-2 py-1 space-y-1">
          <div className="px-3 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Inquiry History
          </div>

          {sessions.length === 0 ? (
            <div className="px-3 py-4 text-xs text-slate-400 text-center italic">
              No previous inquiries recorded.
            </div>
          ) : (
            sessions.map((session) => {
              const isActive = session.id === currentSessionId;
              return (
                <div
                  key={session.id}
                  onClick={() => {
                    onSelectSession(session.id);
                    if (window.innerWidth < 1024) onClose();
                  }}
                  className={`group relative flex items-center justify-between gap-2 px-3 py-2 rounded-lg cursor-pointer text-xs transition-all ${
                    isActive
                      ? 'bg-slate-800 text-white font-medium shadow-sm'
                      : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-2.5 truncate flex-1 min-w-0">
                    <MessageSquare className={`w-3.5 h-3.5 flex-shrink-0 ${isActive ? 'text-justice-400' : 'text-slate-400'}`} />
                    <span className="truncate" title={session.title}>
                      {session.title}
                    </span>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteSession(session.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-rose-500/20 hover:text-rose-400 text-slate-400 transition-all"
                    title="Delete inquiry"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Bottom Utility Tools */}
        <div className="p-3 border-t border-slate-800 space-y-1">
          <button
            onClick={() => {
              onOpenDocuments();
              if (window.innerWidth < 1024) onClose();
            }}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-medium transition-colors"
          >
            <Database className="w-4 h-4 text-emerald-400" />
            <span>Document Vault (Statutes)</span>
          </button>

          <button
            onClick={() => {
              onOpenBookmarks();
              if (window.innerWidth < 1024) onClose();
            }}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-medium transition-colors"
          >
            <Bookmark className="w-4 h-4 text-gold-400" />
            <span>Saved Legal Provisions</span>
          </button>

          <button
            onClick={() => {
              onOpenExport();
              if (window.innerWidth < 1024) onClose();
            }}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-medium transition-colors"
          >
            <Download className="w-4 h-4 text-cyan-400" />
            <span>Export Inquiry Transcript</span>
          </button>
        </div>

        {/* Footer Jurisdiction Emblem Note */}
        <div className="px-4 py-3 bg-slate-950/60 border-t border-slate-800/80 text-[10px] text-slate-400 flex items-center justify-between">
          <span>Jurisdiction: India</span>
          <span className="flex items-center gap-1 font-mono text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            RAG Online
          </span>
        </div>
      </aside>
    </>
  );
}
