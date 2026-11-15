import React, { useState } from 'react';
import { User, Shield, Copy, Check, Bookmark as BookmarkIcon, Share2 } from 'lucide-react';
import SourceCard from './SourceCard';

export default function MessageItem({ message, onBookmark, userQuery }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleBookmarkClick = () => {
    if (onBookmark) {
      onBookmark(message);
    }
  };

  // Basic markdown to formatted elements renderer
  const renderFormattedContent = (content) => {
    if (!content) return null;
    const lines = content.split('\n');

    return lines.map((line, idx) => {
      // Headers
      if (line.startsWith('### ')) {
        return (
          <h3 key={idx} className="text-base font-bold text-slate-900 dark:text-slate-100 mt-3 mb-1.5 font-serif">
            {line.replace('### ', '')}
          </h3>
        );
      }
      if (line.startsWith('#### ')) {
        return (
          <h4 key={idx} className="text-sm font-semibold text-justice-700 dark:text-justice-300 mt-2.5 mb-1 font-serif">
            {line.replace('#### ', '')}
          </h4>
        );
      }
      // Blockquotes
      if (line.startsWith('> ')) {
        return (
          <blockquote
            key={idx}
            className="my-2 border-l-4 border-justice-500 bg-slate-100 dark:bg-slate-900/80 px-3 py-1.5 text-xs text-slate-700 dark:text-slate-300 rounded-r font-mono"
          >
            {line.replace('> ', '')}
          </blockquote>
        );
      }
      // Bullet items
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const text = line.substring(2);
        return (
          <li key={idx} className="ml-4 list-disc text-sm text-slate-700 dark:text-slate-300 my-0.5 leading-relaxed">
            {formatBoldText(text)}
          </li>
        );
      }
      // Empty line spacer
      if (!line.trim()) {
        return <div key={idx} className="h-2" />;
      }

      // Normal paragraph
      return (
        <p key={idx} className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed my-1">
          {formatBoldText(line)}
        </p>
      );
    });
  };

  // Helper to highlight **bold** and *italic*
  const formatBoldText = (text) => {
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-semibold text-slate-900 dark:text-white">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('*') && part.endsWith('*')) {
        return <em key={i} className="text-slate-600 dark:text-slate-400">{part.slice(1, -1)}</em>;
      }
      return part;
    });
  };

  return (
    <div className={`py-4 px-4 sm:px-6 transition-colors ${
      isUser 
        ? 'bg-slate-50/50 dark:bg-slate-950/40' 
        : 'bg-white dark:bg-slate-900/70 border-y border-slate-100 dark:border-slate-800/80'
    }`}>
      <div className="max-w-4xl mx-auto flex gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          {isUser ? (
            <div className="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300">
              <User className="w-4 h-4" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-justice-700 text-white flex items-center justify-center shadow-sm">
              <Shield className="w-4 h-4 text-gold-400" />
            </div>
          )}
        </div>

        {/* Content Body */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              {isUser ? 'Legal Inquirer' : 'AI Justice Department Assistant'}
            </span>
            {!isUser && (
              <div className="flex items-center gap-1">
                <button
                  onClick={copyToClipboard}
                  className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  title="Copy legal response"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
                <button
                  onClick={handleBookmarkClick}
                  className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded text-slate-500 hover:text-justice-600 dark:text-slate-400 dark:hover:text-justice-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  title="Bookmark this statutory provision"
                >
                  <BookmarkIcon className="w-3.5 h-3.5" />
                  <span>Save</span>
                </button>
              </div>
            )}
          </div>

          {/* Text Message */}
          <div className="prose dark:prose-invert max-w-none">
            {renderFormattedContent(message.content)}
          </div>

          {/* Source Citations Drawer/Cards */}
          {!isUser && message.citations && message.citations.length > 0 && (
            <SourceCard citations={message.citations} />
          )}
        </div>
      </div>
    </div>
  );
}
