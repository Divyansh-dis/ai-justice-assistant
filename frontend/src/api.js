import axios from 'axios';

// When running through Vite proxy or directly on port 8000
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Chat
  async sendChat(query, sessionId = null) {
    const res = await client.post('/chat', { query, session_id: sessionId });
    return res.data;
  },

  // Sessions
  async getSessions() {
    const res = await client.get('/sessions');
    return res.data;
  },

  async createSession(title = 'New Legal Inquiry') {
    const res = await client.post('/sessions', { title });
    return res.data;
  },

  async getSession(sessionId) {
    const res = await client.get(`/sessions/${sessionId}`);
    return res.data;
  },

  async deleteSession(sessionId) {
    const res = await client.delete(`/sessions/${sessionId}`);
    return res.data;
  },

  // Documents
  async getDocuments() {
    const res = await client.get('/documents');
    return res.data;
  },

  async triggerIngestion() {
    const res = await client.post('/documents/ingest');
    return res.data;
  },

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await client.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  // Bookmarks
  async getBookmarks() {
    const res = await client.get('/bookmarks');
    return res.data;
  },

  async addBookmark(data) {
    const res = await client.post('/bookmarks', data);
    return res.data;
  },

  async deleteBookmark(bookmarkId) {
    const res = await client.delete(`/bookmarks/${bookmarkId}`);
    return res.data;
  },

  // Health
  async getHealth() {
    const res = await client.get('/health');
    return res.data;
  },
};

export default api;
