import React from 'react';
import { X, Download, Printer, FileText, Check } from 'lucide-react';

export default function ExportModal({ isOpen, onClose, sessionTitle, messages }) {
  if (!isOpen) return null;

  const generateMarkdown = () => {
    let md = `# Legal Inquiry Transcript - AI Justice Department Assistant\n`;
    md += `**Jurisdiction:** Republic of India (Statutes & Acts)\n`;
    md += `**Session Title:** ${sessionTitle || 'Legal Inquiry'}\n`;
    md += `**Export Date:** ${new Date().toLocaleString()}\n`;
    md += `**System:** AI Justice Department Assistant Legal RAG\n\n`;
    md += `---\n\n`;

    messages.forEach((m, idx) => {
      const speaker = m.role === 'user' ? 'LEGAL INQUIRER' : 'AI JUSTICE ASSISTANT';
      md += `### ${speaker} (${new Date(m.created_at || Date.now()).toLocaleTimeString()}):\n\n`;
      md += `${m.content}\n\n`;

      if (m.citations && m.citations.length > 0) {
        md += `#### Verified Statutory Citations:\n`;
        m.citations.forEach((c, cIdx) => {
          md += `${cIdx + 1}. **${c.title}** - *${c.section}* (Page ${c.page}, Match: ${Math.round(c.relevance_score * 100)}%)\n`;
          md += `   > ${c.snippet.replace(/\n/g, ' ')}\n`;
        });
        md += `\n`;
      }
      md += `---\n\n`;
    });

    md += `\n*Disclaimer: This document is an automated transcript from the AI Justice Department Assistant. For official court proceedings, please refer to the official Gazette of India.*\n`;
    return md;
  };

  const handleDownloadMarkdown = () => {
    const md = generateMarkdown();
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Legal_Transcript_${(sessionTitle || 'Session').replace(/[^a-zA-Z0-9]/g, '_')}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center border border-cyan-500/20">
              <Download className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white font-serif">
                Export Legal Inquiry Session
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Export transcript with verified statutory citations for legal documentation.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 overflow-y-auto space-y-4">
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950/70 border border-slate-200 dark:border-slate-800 space-y-2">
            <div className="text-xs font-semibold text-slate-700 dark:text-slate-300">
              Session Overview:
            </div>
            <div className="text-sm font-bold text-slate-900 dark:text-white font-serif">
              {sessionTitle || "Current Legal Inquiry"}
            </div>
            <div className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-4">
              <span>{messages.length} Total Messages</span>
              <span>•</span>
              <span>{messages.filter(m => m.citations?.length > 0).length} Statutory Citations</span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Markdown Export Card */}
            <div
              onClick={handleDownloadMarkdown}
              className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-justice-400 hover:shadow-sm cursor-pointer transition-all flex flex-col justify-between group"
            >
              <div>
                <div className="w-8 h-8 rounded-lg bg-justice-100 text-justice-700 dark:bg-justice-950 dark:text-justice-300 flex items-center justify-center mb-3">
                  <FileText className="w-4 h-4" />
                </div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-justice-600 dark:group-hover:text-justice-400 transition-colors">
                  Markdown (.md)
                </h4>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  Formatted legal transcript suitable for drafting in Obsidian, Notion, or GitHub.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center text-xs font-semibold text-justice-600 dark:text-justice-400 gap-1">
                <Download className="w-3.5 h-3.5" />
                <span>Download .md</span>
              </div>
            </div>

            {/* Print / PDF Export Card */}
            <div
              onClick={handlePrint}
              className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-justice-400 hover:shadow-sm cursor-pointer transition-all flex flex-col justify-between group"
            >
              <div>
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 flex items-center justify-center mb-3">
                  <Printer className="w-4 h-4" />
                </div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                  Print to PDF
                </h4>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  Direct browser print dialog to save as an official government-grade PDF file.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center text-xs font-semibold text-emerald-600 dark:text-emerald-400 gap-1">
                <Printer className="w-3.5 h-3.5" />
                <span>Open Print Dialog</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-xs font-medium bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
