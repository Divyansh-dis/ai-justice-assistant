import React, { useState, useEffect } from 'react';
import { 
  X, 
  Bookmark as BookmarkIcon, 
  Trash2, 
  Copy, 
  Check, 
  BookOpen, 
  Calendar 
} from 'lucide-react';
import api from '../api';

export default function BookmarksModal({
  isOpen,
  onClose,
  activeBookmarkData,
  onClearActiveBookmark
}) {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  
  // New bookmark form state (when bookmarking from message)
  const [noteInput, setNoteInput] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadBookmarks();
    }
  }, [isOpen]);

  const loadBookmarks = async () => {
    setLoading(true);
    try {
      const data = await api.getBookmarks();
      setBookmarks(data);
    } catch (err) {
      console.error("Failed to load bookmarks", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveNewBookmark = async (e) => {
    e.preventDefault();
    if (!activeBookmarkData) return;

    setSaving(true);
    try {
      const firstCitation = activeBookmarkData.citations?.[0];
      await api.addBookmark({
        session_id: activeBookmarkData.session_id,
        message_id: activeBookmarkData.id,
        query: activeBookmarkData.query || "Legal Query",
        answer: activeBookmarkData.content,
        statute_title: firstCitation?.title || "Indian Legal Statute",
        section_ref: firstCitation?.section || "General",
        note: noteInput.trim() || undefined
      });
      setNoteInput('');
      onClearActiveBookmark();
      await loadBookmarks();
    } catch (err) {
      console.error("Failed to save bookmark", err);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteBookmark(id);
      setBookmarks(bookmarks.filter(b => b.id !== id));
    } catch (err) {
      console.error("Failed to delete bookmark", err);
    }
  };

  const copyAnswer = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gold-500/10 text-gold-500 flex items-center justify-center border border-gold-500/20">
              <BookmarkIcon className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white font-serif">
                Saved Legal Provisions & Answers
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Bookmarked statutory analyses for rapid citation and legal drafting.
              </p>
            </div>
          </div>
          <button
            onClick={() => {
              if (onClearActiveBookmark) onClearActiveBookmark();
              onClose();
            }}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form to Save Active Bookmark if triggered from chat */}
        {activeBookmarkData && (
          <form onSubmit={handleSaveNewBookmark} className="p-4 bg-justice-50 dark:bg-slate-950/80 border-b border-justice-200 dark:border-justice-900">
            <h4 className="text-xs font-bold text-justice-800 dark:text-justice-300 uppercase tracking-wide mb-2">
              Save Current Legal Answer
            </h4>
            <div className="flex gap-2">
              <input
                type="text"
                value={noteInput}
                onChange={(e) => setNoteInput(e.target.value)}
                placeholder="Optional annotation (e.g., Key precedent for BNS Section 303 defense)..."
                className="flex-1 text-xs px-3 py-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 focus:outline-none focus:ring-1 focus:ring-justice-500 text-slate-900 dark:text-white"
              />
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-2 bg-justice-600 hover:bg-justice-700 text-white rounded-lg text-xs font-medium shadow-sm transition-colors"
              >
                {saving ? 'Saving...' : 'Confirm Bookmark'}
              </button>
              <button
                type="button"
                onClick={onClearActiveBookmark}
                className="px-3 py-2 text-xs text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {/* Bookmarks List */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3">
          {loading ? (
            <div className="text-center py-10 text-xs text-slate-400">Loading saved bookmarks...</div>
          ) : bookmarks.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-xs">
              No bookmarked provisions yet. Click the "Save" button on any legal answer to bookmark it here.
            </div>
          ) : (
            bookmarks.map((bm) => (
              <div
                key={bm.id}
                className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs space-y-2"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2 flex-wrap">
                    {bm.section_ref && (
                      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-justice-100 text-justice-800 dark:bg-justice-950 dark:text-justice-300">
                        {bm.section_ref}
                      </span>
                    )}
                    {bm.statute_title && (
                      <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
                        {bm.statute_title}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => copyAnswer(bm.answer, bm.id)}
                      className="p-1.5 rounded text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      title="Copy Answer"
                    >
                      {copiedId === bm.id ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                    <button
                      onClick={() => handleDelete(bm.id)}
                      className="p-1.5 rounded text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                      title="Delete Bookmark"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {bm.note && (
                  <div className="p-2 bg-amber-50 dark:bg-amber-950/40 border-l-2 border-amber-500 text-amber-900 dark:text-amber-200 text-xs rounded-r">
                    <strong className="font-semibold">Annotation: </strong> {bm.note}
                  </div>
                )}

                <div className="bg-slate-50 dark:bg-slate-950/60 p-3 rounded-lg border border-slate-200 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 font-sans leading-relaxed line-clamp-4">
                  {bm.answer}
                </div>

                <div className="flex items-center gap-2 text-[10px] text-slate-400">
                  <Calendar className="w-3 h-3" />
                  <span>Saved on {new Date(bm.created_at).toLocaleString()}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800 flex justify-end">
          <button
            onClick={() => {
              if (onClearActiveBookmark) onClearActiveBookmark();
              onClose();
            }}
            className="px-4 py-2 rounded-lg text-xs font-medium bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
