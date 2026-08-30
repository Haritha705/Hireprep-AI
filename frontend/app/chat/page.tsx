'use client';

import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '@/lib/api';

export default function ChatPage() {
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'ai'; text: string }>>([
    {
      sender: 'ai',
      text: 'Hello! I am HirePrep AI Assistant. I can help you practice Python algorithms, SQL queries, Generative AI architecture, resume optimization, or mock technical interviews. How can I help you today?',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const suggestedPrompts = [
    'Give me Python interview questions',
    'Test my SQL skills',
    'Ask me GenAI scenario questions',
    'Start a mock interview',
    'Ask questions based on my resume',
    'Identify my weak areas',
  ];

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input.trim();
    if (!query || loading) return;

    if (!textToSend) setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(query);
      const aiReply = res.data.response || 'Sorry, I could not process that request.';
      setMessages((prev) => [...prev, { sender: 'ai', text: aiReply }]);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Error connecting to AI chat service. Please ensure the backend is running.';
      setMessages((prev) => [...prev, { sender: 'ai', text: `Error: ${msg}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        sender: 'ai',
        text: 'Conversation cleared. What topic would you like to prepare for next?',
      },
    ]);
  };

  return (
    <div className="container py-4">
      <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
        <div>
          <h2 className="fw-bold text-white mb-1">AI Career & Interview Assistant</h2>
          <p className="text-subtle mb-0" style={{ fontSize: '0.92rem' }}>
            Interactive AI practice partner for technical coding, SQL, GenAI concepts, and interview prep.
          </p>
        </div>
        <button className="btn btn-saas-outline py-1 px-3" onClick={handleClear} style={{ fontSize: '0.82rem' }}>
          🗑️ Clear Conversation
        </button>
      </div>

      {/* ── SUGGESTED PROMPT CHIPS ── */}
      <div className="saas-card p-3 mb-3">
        <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }} className="mb-2">
          Suggested Practice Prompts
        </div>
        <div className="d-flex flex-wrap gap-2">
          {suggestedPrompts.map((prompt, idx) => (
            <button
              key={idx}
              className="badge-indigo text-start border-0"
              style={{ padding: '6px 12px', cursor: 'pointer', fontSize: '0.82rem' }}
              onClick={() => handleSend(prompt)}
              disabled={loading}
            >
              💡 {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* ── CHAT MESSAGES WINDOW ── */}
      <div className="row justify-content-center">
        <div className="col-lg-10">
          <div className="saas-card p-4 d-flex flex-column" style={{ height: '520px' }}>
            {/* Messages Area */}
            <div className="flex-grow-1 overflow-auto pe-2 d-flex flex-column gap-3 mb-3">
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`d-flex gap-2 ${m.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
                >
                  <div
                    className="p-3 rounded-3"
                    style={{
                      maxWidth: '82%',
                      fontSize: '0.92rem',
                      lineHeight: '1.6',
                      whiteSpace: 'pre-wrap',
                      backgroundColor: m.sender === 'user' ? 'var(--surface)' : 'var(--bg-subtle)',
                      border: `1px solid ${m.sender === 'user' ? 'var(--primary)' : 'var(--border)'}`,
                      color: m.sender === 'user' ? '#ffffff' : 'var(--text-body)',
                    }}
                  >
                    <div
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: '700',
                        marginBottom: '6px',
                        color: m.sender === 'user' ? 'var(--primary)' : 'var(--violet)',
                        letterSpacing: '0.05em',
                      }}
                    >
                      {m.sender === 'user' ? 'YOU' : 'HIREPREP AI ASSISTANT'}
                    </div>
                    {m.text}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="d-flex align-items-center gap-2 p-2" style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>
                  <div className="spinner-border spinner-border-sm text-primary" role="status"></div>
                  HirePrep AI is processing your answer...
                </div>
              )}
              <div ref={scrollRef} />
            </div>

            {/* Input Form */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="d-flex gap-2"
            >
              <input
                type="text"
                className="form-control"
                placeholder="Ask about Python, SQL, GenAI scenarios, or mock questions..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
              />
              <button type="submit" className="btn btn-saas-primary px-4" disabled={loading || !input.trim()}>
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
