import axios, { InternalAxiosRequestConfig } from 'axios';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
});

// Interceptor to attach JWT token if available
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('hireprep_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// ── Auth ─────────────────────────────────────────────────────
export const signUpUser = (data: { full_name: string; email: string; password: string }) =>
  api.post('/auth/signup', data);

export const loginUser = (data: { email: string; password: string }) =>
  api.post('/auth/login', data);

export const getMe = () => api.get('/auth/me');

// ── Health ──────────────────────────────────────────────────
export const checkHealth = () => api.get('/health/');

// ── Upload ──────────────────────────────────────────────────
export const uploadResume = (file: File) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post('/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};

// ── Chat ─────────────────────────────────────────────────────
export const sendChatMessage = (message: string) =>
  api.post('/chat', { message }, { timeout: 120000 });

// ── Interview Prep ───────────────────────────────────────────
export const generateInterviewQuestions = (skills: string, projects: string) =>
  api.post('/interview', { skills, projects });

// ── Evaluation ───────────────────────────────────────────────
export const evaluateAnswer = (question: string, answer: string, resume_context = '') =>
  api.post('/evaluation', { question, answer, resume_context });

// ── Voice Interview ──────────────────────────────────────────
export const startVoiceInterview = (resume: File | null, resumeText: string) => {
  const fd = new FormData();
  if (resume) fd.append('resume', resume);
  else fd.append('resume_text', resumeText);
  return api.post('/voice/interview/start', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};

export const respondToInterview = (sessionId: string, audioBlob: Blob) => {
  const fd = new FormData();
  fd.append('session_id', sessionId);
  fd.append('audio', audioBlob, 'answer.webm');
  return api.post('/voice/interview/respond', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
};

export const getInterviewSummary = (sessionId: string) =>
  api.get(`/voice/interview/summary/${sessionId}`);

export const getAudioUrl = (sessionId: string, filename: string) =>
  `${BASE_URL}/voice/interview/audio/${sessionId}/${filename}`;
