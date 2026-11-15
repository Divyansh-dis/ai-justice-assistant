import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import DocumentModal from './components/DocumentModal';
import BookmarksModal from './components/BookmarksModal';
import ExportModal from './components/ExportModal';
import api from './api';

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [currentSessionTitle, setCurrentSessionTitle] = useState('New Legal Inquiry');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [vectorCount, setVectorCount] = useState(0);

  // Modals state
  const [documentModalOpen, setDocumentModalOpen] = useState(false);
  const [bookmarksModalOpen, setBookmarksModalOpen] = useState(false);
  const [exportModalOpen, setExportModalOpen] = useState(false);
  const [activeBookmarkData, setActiveBookmarkData] = useState(null);

  // Dark mode state
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('justice_assistant_theme') === 'dark';
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('justice_assistant_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('justice_assistant_theme', 'light');
    }
  }, [darkMode]);

  // Initial load
  useEffect(() => {
    fetchSessions();
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const data = await api.getHealth();
      setVectorCount(data.vector_chunks_indexed || 0);
    } catch (err) {
      console.warn("Backend health check warning:", err.message);
    }
  };

  const fetchSessions = async () => {
    try {
      const data = await api.getSessions();
      setSessions(data);
    } catch (err) {
      console.error("Failed to load sessions:", err);
    }
  };

  const handleSelectSession = async (sessionId) => {
    if (sessionId === currentSessionId) return;
    setIsLoading(true);
    try {
      const sessionDetail = await api.getSession(sessionId);
      setCurrentSessionId(sessionId);
      setCurrentSessionTitle(sessionDetail.title);
      setMessages(sessionDetail.messages || []);
    } catch (err) {
      console.error("Failed to fetch session detail:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSession = () => {
    setCurrentSessionId(null);
    setCurrentSessionTitle('New Legal Inquiry');
    setMessages([]);
  };

  const handleDeleteSession = async (sessionId) => {
    try {
      await api.deleteSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        handleNewSession();
      }
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };

  const handleSendMessage = async (queryText) => {
    if (!queryText.trim() || isLoading) return;

    // Optimistic user message
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: queryText,
      created_at: new Date().toISOString(),
      citations: []
    };

    setMessages(prev => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      const response = await api.sendChat(queryText, currentSessionId);
      
      // Update session ID if this was a new session
      if (!currentSessionId) {
        setCurrentSessionId(response.session_id);
        setCurrentSessionTitle(queryText.slice(0, 48));
        fetchSessions();
      }

      const assistantMsg = {
        id: `assistant-${Date.now()}`,
        session_id: response.session_id,
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        created_at: response.created_at
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Chat request failed:", err);
      const errorMsg = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: "An error occurred while connecting to the legal RAG engine. Please ensure the backend service is running and vector database is initialized.",
        citations: []
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenBookmarkDialog = (message) => {
    // Find the preceding user query
    const msgIndex = messages.findIndex(m => m.id === message.id);
    let userQuery = "Legal Query";
    for (let i = msgIndex - 1; i >= 0; i--) {
      if (messages[i].role === 'user') {
        userQuery = messages[i].content;
        break;
      }
    }

    setActiveBookmarkData({
      ...message,
      query: userQuery
    });
    setBookmarksModalOpen(true);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 font-sans">
      {/* Collapsible Left Sidebar */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={handleSelectSession}
        onNewSession={handleNewSession}
        onDeleteSession={handleDeleteSession}
        onOpenDocuments={() => setDocumentModalOpen(true)}
        onOpenBookmarks={() => {
          setActiveBookmarkData(null);
          setBookmarksModalOpen(true);
        }}
        onOpenExport={() => setExportModalOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:ml-72 transition-all">
        {/* Top Government-Grade Navbar */}
        <Navbar
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          darkMode={darkMode}
          onToggleDarkMode={() => setDarkMode(!darkMode)}
          onOpenDocuments={() => setDocumentModalOpen(true)}
          onOpenBookmarks={() => {
            setActiveBookmarkData(null);
            setBookmarksModalOpen(true);
          }}
          vectorCount={vectorCount}
        />

        {/* Central Chat Interface */}
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSendMessage={handleSendMessage}
          onBookmark={handleOpenBookmarkDialog}
        />
      </div>

      {/* Document Management Vault Modal */}
      <DocumentModal
        isOpen={documentModalOpen}
        onClose={() => setDocumentModalOpen(false)}
        onRefreshStats={fetchHealth}
      />

      {/* Bookmarks Modal */}
      <BookmarksModal
        isOpen={bookmarksModalOpen}
        onClose={() => {
          setBookmarksModalOpen(false);
          setActiveBookmarkData(null);
        }}
        activeBookmarkData={activeBookmarkData}
        onClearActiveBookmark={() => setActiveBookmarkData(null)}
      />

      {/* Export Modal */}
      <ExportModal
        isOpen={exportModalOpen}
        onClose={() => setExportModalOpen(false)}
        sessionTitle={currentSessionTitle}
        messages={messages}
      />
    </div>
  );
}
