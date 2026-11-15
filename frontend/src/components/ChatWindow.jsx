import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Scale, 
  Sparkles, 
  BookOpen, 
  AlertCircle, 
  ShieldCheck, 
  FileText,
  Loader2,
  HelpCircle
} from 'lucide-react';
import MessageItem from './MessageItem';

const SUGGESTED_QUERIES = [
  {
    title: "Bharatiya Nyaya Sanhita (BNS 2023)",
    query: "What are the punishments prescribed for theft and murder under Bharatiya Nyaya Sanhita?",
    icon: Scale
  },
  {
    title: "Cyber Law & IT Act 2000",
    query: "What are the legal penalties for identity theft and hacking under Sections 43 and 66C of the IT Act?",
    icon: FileText
  },
  {
    title: "Right to Information (RTI 2005)",
    query: "What is the timeline for disposal of an RTI request, and what are the penalties for delayed response under Section 20?",
    icon: BookOpen
  },
  {
    title: "Fundamental Rights (Constitution)",
    query: "Explain the scope of Right to Life and Personal Liberty under Article 21 of the Indian Constitution.",
    icon: ShieldCheck
  },
  {
    title: "Data Protection (DPDP Act 2023)",
    query: "What are the conditions for valid consent and the penalties for data breach under the Digital Personal Data Protection Act 2023?",
    icon: Sparkles
  }
];

export default function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  onBookmark
}) {
  const [inputQuery, setInputQuery] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!inputQuery.trim() || isLoading) return;

    onSendMessage(inputQuery.trim());
    setInputQuery('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextareaInput = (e) => {
    setInputQuery(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  const handleSuggestionClick = (query) => {
    if (isLoading) return;
    onSendMessage(query);
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 dark:bg-slate-950 overflow-hidden relative">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          /* Empty State Welcome Screen */
          <div className="max-w-3xl mx-auto px-4 py-8 sm:py-12 flex flex-col items-center text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-justice-800 to-justice-950 text-gold-400 flex items-center justify-center shadow-lg border border-gold-500/30 mb-5">
              <Scale className="w-8 h-8 text-gold-400" />
            </div>

            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white font-serif tracking-tight">
              AI Justice Department Legal Assistant
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-xl leading-relaxed">
              Autonomous legal RAG query engine grounded strictly in verified public Indian statutes, Bharatiya Nyaya Sanhita, Parliamentary Acts, and Constitutional Articles.
            </p>

            {/* Anti-Hallucination Assurance Banner */}
            <div className="mt-5 w-full max-w-xl p-3 rounded-lg bg-justice-50 dark:bg-slate-900/90 border border-justice-200 dark:border-justice-800 flex items-start gap-2.5 text-left">
              <ShieldCheck className="w-5 h-5 text-justice-700 dark:text-justice-400 flex-shrink-0 mt-0.5" />
              <div className="text-xs">
                <span className="font-semibold text-justice-900 dark:text-justice-200">Strict Anti-Hallucination Policy: </span>
                <span className="text-slate-600 dark:text-slate-400">
                  Answers are derived strictly from retrieved statute chunks with exact section and page citations.
                </span>
              </div>
            </div>

            {/* Suggested Sample Queries */}
            <div className="mt-8 w-full">
              <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3 text-left">
                <HelpCircle className="w-4 h-4 text-justice-600 dark:text-justice-400" />
                <span>Explore Key Indian Statutory Queries</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
                {SUGGESTED_QUERIES.map((sq, idx) => {
                  const Icon = sq.icon;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSuggestionClick(sq.query)}
                      className="p-3.5 rounded-xl border border-slate-200 bg-white hover:border-justice-400 hover:shadow-sm dark:border-slate-800 dark:bg-slate-900/80 dark:hover:border-justice-600 text-left transition-all group"
                    >
                      <div className="flex items-center gap-2 text-xs font-semibold text-justice-700 dark:text-justice-300 mb-1">
                        <Icon className="w-3.5 h-3.5 text-gold-500" />
                        <span>{sq.title}</span>
                      </div>
                      <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2 leading-snug group-hover:text-slate-900 dark:group-hover:text-slate-200">
                        {sq.query}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          /* Render Message History */
          <div className="divide-y divide-slate-100 dark:divide-slate-800/60 pb-6">
            {messages.map((msg, index) => (
              <MessageItem
                key={msg.id || index}
                message={msg}
                onBookmark={onBookmark}
              />
            ))}

            {/* In-Flight Retrieval / Generation Loader */}
            {isLoading && (
              <div className="py-6 px-4 sm:px-6 bg-white dark:bg-slate-900/70 border-t border-slate-100 dark:border-slate-800">
                <div className="max-w-4xl mx-auto flex items-start gap-4">
                  <div className="w-8 h-8 rounded-full bg-justice-700 text-white flex items-center justify-center flex-shrink-0 animate-pulse">
                    <Scale className="w-4 h-4 text-gold-400" />
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-2 text-xs font-medium text-justice-700 dark:text-justice-400">
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Querying ChromaDB vector database & synthesizing legal provisions...</span>
                    </div>
                    <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-3/4 animate-pulse" />
                    <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-1/2 animate-pulse" />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Bar & Footer Container */}
      <div className="border-t border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md px-4 py-3 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative flex items-end gap-2 bg-slate-100 dark:bg-slate-950 rounded-xl p-2 border border-slate-300 dark:border-slate-800 focus-within:border-justice-500 focus-within:ring-1 focus-within:ring-justice-500 transition-all">
            <textarea
              ref={textareaRef}
              rows={1}
              value={inputQuery}
              onChange={handleTextareaInput}
              onKeyDown={handleKeyDown}
              placeholder="Inquire on legal statutes, sections, penalties, or rights (e.g. RTI timelines, IT Act offences, Article 21)..."
              className="flex-1 max-h-36 resize-none bg-transparent px-2.5 py-1.5 text-xs sm:text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none leading-relaxed"
            />
            <button
              type="submit"
              disabled={!inputQuery.trim() || isLoading}
              className={`p-2.5 rounded-lg flex items-center justify-center transition-all ${
                inputQuery.trim() && !isLoading
                  ? 'bg-justice-600 hover:bg-justice-700 text-white shadow-sm'
                  : 'bg-slate-200 text-slate-400 dark:bg-slate-800 dark:text-slate-600 cursor-not-allowed'
              }`}
              title="Send Inquiry"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </button>
          </form>

          {/* Legal Disclaimer Footer */}
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 px-1">
            <span className="flex items-center gap-1">
              <AlertCircle className="w-3 h-3 text-gold-500" />
              <span>Grounded in Indian Legal Corpus. Answers reference statutory provisions.</span>
            </span>
            <span className="hidden sm:inline font-mono text-[10px]">
              Press <kbd className="px-1 py-0.5 bg-slate-200 dark:bg-slate-800 rounded text-[9px]">Enter</kbd> to submit
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
