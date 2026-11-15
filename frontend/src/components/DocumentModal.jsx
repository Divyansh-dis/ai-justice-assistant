import React, { useState, useEffect, useRef } from 'react';
import { 
  X, 
  Database, 
  Upload, 
  RefreshCw, 
  FileText, 
  CheckCircle2, 
  AlertCircle,
  HardDrive,
  Layers,
  Calendar
} from 'lucide-react';
import api from '../api';

export default function DocumentModal({ isOpen, onClose, onRefreshStats }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      loadDocuments();
    }
  }, [isOpen]);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const data = await api.getDocuments();
      setDocuments(data);
    } catch (err) {
      console.error("Failed to load documents", err);
    } finally {
      setLoading(false);
    }
  };

  const handleReIngest = async () => {
    setIngesting(true);
    setMessage(null);
    try {
      const res = await api.triggerIngestion();
      setMessage({ type: 'success', text: `Ingestion complete! ${res.total_chunks} chunks indexed across ${res.documents_processed} statutes.` });
      await loadDocuments();
      if (onRefreshStats) onRefreshStats();
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to re-index documents.' });
    } finally {
      setIngesting(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setMessage({ type: 'error', text: 'Please select a valid PDF statute document.' });
      return;
    }

    setUploading(true);
    setMessage(null);
    try {
      await api.uploadDocument(file);
      setMessage({ type: 'success', text: `Successfully vectorized and indexed "${file.name}"!` });
      await loadDocuments();
      if (onRefreshStats) onRefreshStats();
    } catch (err) {
      setMessage({ type: 'error', text: 'Document upload and indexing failed.' });
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  if (!isOpen) return null;

  const totalChunks = documents.reduce((sum, d) => sum + d.chunk_count, 0);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-justice-600 text-white flex items-center justify-center shadow-md">
              <Database className="w-5 h-5 text-gold-400" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white font-serif">
                Legal Document Vault & Ingestion
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Vectorized Indian legal statutes, Acts of Parliament, and Constitutional text.
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

        {/* Modal Subheader Stats & Actions */}
        <div className="px-5 py-3.5 bg-slate-50 dark:bg-slate-950/60 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5 text-slate-700 dark:text-slate-300">
              <FileText className="w-4 h-4 text-justice-600 dark:text-justice-400" />
              <span className="font-semibold">{documents.length}</span> Statutes Loaded
            </div>
            <div className="flex items-center gap-1.5 text-slate-700 dark:text-slate-300">
              <Layers className="w-4 h-4 text-emerald-500" />
              <span className="font-semibold">{totalChunks}</span> Vector Chunks
            </div>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".pdf"
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-750 shadow-sm transition-all"
            >
              <Upload className="w-3.5 h-3.5 text-justice-600 dark:text-justice-400" />
              <span>{uploading ? 'Ingesting PDF...' : 'Upload Statute PDF'}</span>
            </button>

            <button
              onClick={handleReIngest}
              disabled={ingesting}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-justice-600 hover:bg-justice-700 text-white shadow-sm transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${ingesting ? 'animate-spin' : ''}`} />
              <span>{ingesting ? 'Indexing...' : 'Re-Index All'}</span>
            </button>
          </div>
        </div>

        {/* Status Alert Message */}
        {message && (
          <div className={`mx-5 mt-3 p-3 rounded-lg text-xs flex items-center gap-2 ${
            message.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800'
              : 'bg-rose-50 text-rose-800 border border-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:border-rose-800'
          }`}>
            {message.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
            )}
            <span>{message.text}</span>
          </div>
        )}

        {/* Documents Table / List */}
        <div className="flex-1 overflow-y-auto p-5">
          {loading ? (
            <div className="text-center py-10 text-xs text-slate-400">Loading statutory index...</div>
          ) : documents.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-xs">
              No legal documents found in repository. Click "Re-Index All" or upload a PDF statute.
            </div>
          ) : (
            <div className="space-y-2.5">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="p-3.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 flex items-start justify-between gap-3 shadow-xs"
                >
                  <div className="flex items-start gap-3 min-w-0">
                    <div className="w-9 h-9 rounded-lg bg-justice-50 dark:bg-slate-800 text-justice-700 dark:text-justice-400 flex items-center justify-center flex-shrink-0 mt-0.5 border border-justice-200/60 dark:border-slate-700">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="text-xs sm:text-sm font-semibold text-slate-900 dark:text-white truncate" title={doc.title}>
                        {doc.title}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono mt-0.5">
                        {doc.filename}
                      </p>
                      <div className="flex items-center gap-3 mt-1.5 text-[11px] text-slate-400 flex-wrap">
                        <span className="flex items-center gap-1">
                          <HardDrive className="w-3 h-3" />
                          <span>{(doc.file_size_bytes / 1024).toFixed(1)} KB</span>
                        </span>
                        <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                          <Layers className="w-3 h-3" />
                          <span>{doc.chunk_count} Chunks</span>
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          <span>{new Date(doc.ingested_at).toLocaleDateString()}</span>
                        </span>
                      </div>
                    </div>
                  </div>

                  <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                    Vectorized
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-xs font-medium bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 transition-colors"
          >
            Close Vault
          </button>
        </div>
      </div>
    </div>
  );
}
