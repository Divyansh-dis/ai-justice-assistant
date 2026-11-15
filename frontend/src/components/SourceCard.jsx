import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, Copy, Check, FileText } from 'lucide-react';

export default function SourceCard({ citations }) {
  const [expandedIndex, setExpandedIndex] = useState(null);
  const [copiedIndex, setCopiedIndex] = useState(null);

  if (!citations || citations.length === 0) return null;

  const toggleExpand = (idx) => {
    setExpandedIndex(expandedIndex === idx ? null : idx);
  };

  const copySnippet = (text, idx, e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800">
      <div className="flex items-center gap-2 mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
        <BookOpen className="w-4 h-4 text-justice-600 dark:text-justice-400" />
        <span>Verified Legal Citations ({citations.length} Sources)</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
        {citations.map((c, idx) => {
          const isExpanded = expandedIndex === idx;
          const matchPercent = Math.round(c.relevance_score * 100);

          return (
            <div
              key={idx}
              onClick={() => toggleExpand(idx)}
              className={`text-left p-3 rounded-lg border transition-all cursor-pointer select-none ${
                isExpanded
                  ? 'bg-justice-50/70 border-justice-300 shadow-sm dark:bg-slate-900 dark:border-justice-700'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50/70 dark:bg-slate-900/60 dark:border-slate-800 dark:hover:border-slate-700'
              }`}
            >
              {/* Card Header */}
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-justice-100 text-justice-800 dark:bg-justice-950 dark:text-justice-300">
                      {c.section || 'General Provision'}
                    </span>
                    <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                      Page {c.page}
                    </span>
                    <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-400 dark:border-emerald-800">
                      {matchPercent}% Match
                    </span>
                  </div>
                  <h4 className="mt-1 text-xs font-semibold text-slate-800 dark:text-slate-200 truncate" title={c.title}>
                    {c.title}
                  </h4>
                </div>

                <div className="flex items-center gap-1 text-slate-400">
                  <button
                    onClick={(e) => copySnippet(c.snippet, idx, e)}
                    className="p-1 hover:text-justice-600 dark:hover:text-justice-400 rounded transition-colors"
                    title="Copy statutory text"
                  >
                    {copiedIndex === idx ? (
                      <Check className="w-3.5 h-3.5 text-emerald-500" />
                    ) : (
                      <Copy className="w-3.5 h-3.5" />
                    )}
                  </button>
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-slate-500" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-500" />
                  )}
                </div>
              </div>

              {/* Collapsed Snippet Preview */}
              {!isExpanded && (
                <p className="mt-1.5 text-xs text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed font-sans">
                  {c.snippet}
                </p>
              )}

              {/* Expanded Full Drawer */}
              {isExpanded && (
                <div className="mt-2.5 pt-2 border-t border-justice-200/60 dark:border-slate-800 text-xs">
                  <div className="flex items-center gap-1 text-[11px] text-slate-400 mb-1">
                    <FileText className="w-3 h-3" />
                    <span>File: {c.document_name}</span>
                  </div>
                  <div className="bg-slate-50 dark:bg-slate-950/80 p-2.5 rounded border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-mono text-[11px] leading-relaxed max-h-48 overflow-y-auto whitespace-pre-wrap">
                    {c.snippet}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
