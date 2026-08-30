'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { checkHealth } from '@/lib/api';
import { useAuth } from '@/components/AuthContext';

export default function DashboardPage() {
  const { user } = useAuth();
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth()
      .then((res) => setHealth(res.data))
      .catch(() => setHealth({ status: 'Error', backend: 'Offline' }))
      .finally(() => setLoading(false));
  }, []);

  const categories = [
    { label: 'Python', color: 'rgba(6,182,212,0.15)', border: 'rgba(6,182,212,0.3)', text: '#67E8F9' },
    { label: 'SQL', color: 'rgba(16,185,129,0.15)', border: 'rgba(16,185,129,0.3)', text: '#6EE7B7' },
    { label: 'Data Analytics', color: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.3)', text: '#FCD34D' },
    { label: 'GenAI', color: 'rgba(139,92,246,0.15)', border: 'rgba(139,92,246,0.3)', text: '#C084FC' },
    { label: 'RAG', color: 'rgba(236,72,153,0.15)', border: 'rgba(236,72,153,0.3)', text: '#F9A8D4' },
    { label: 'Machine Learning', color: 'rgba(124,58,237,0.15)', border: 'rgba(124,58,237,0.3)', text: '#A78BFA' },
    { label: 'HR & Behavioral', color: 'rgba(239,68,68,0.15)', border: 'rgba(239,68,68,0.3)', text: '#FCA5A5' },
  ];

  const metrics = [
    {
      label: 'RESUME STATUS',
      value: 'Active / Ready',
      sub: '✔ Vector RAG Synced',
      subColor: 'var(--emerald)',
      accent: '#10B981',
      icon: '📄',
    },
    {
      label: 'SELECTED ROLE',
      value: 'Software Engineer',
      sub: 'Auto-Detected',
      subColor: '#C084FC',
      accent: '#8B5CF6',
      icon: '🎯',
    },
    {
      label: 'VOICE SESSIONS',
      value: '35 Questions',
      sub: 'Live STT + TTS',
      subColor: '#67E8F9',
      accent: '#06B6D4',
      icon: '🎙️',
    },
    {
      label: 'EVALUATION SCORE',
      value: '8.5 / 10 Avg',
      sub: 'High Technical Rank',
      subColor: 'var(--emerald)',
      accent: '#F59E0B',
      icon: '⭐',
    },
  ];

  const quickActions = [
    {
      icon: '🎙️',
      title: 'Voice Interview',
      badge: 'Real-Time Practice',
      badgeClass: 'badge-indigo',
      desc: 'Practice live 35-question oral mock interviews with Groq Whisper speech recognition and Edge-TTS spoken questions.',
      href: '/voice-interview',
      btnText: 'Start Voice Session',
      btnClass: 'btn-luxury-primary',
      gradient: 'linear-gradient(135deg, rgba(124,58,237,0.12), rgba(139,92,246,0.06))',
      borderGlow: 'rgba(139,92,246,0.3)',
    },
    {
      icon: '📄',
      title: 'Resume Parser & RAG',
      badge: 'MongoDB Vector DB',
      badgeClass: 'badge-emerald',
      desc: 'Upload your resume PDF to extract skills and retrieve technical, project, and HR questions matched from your vector store.',
      href: '/upload',
      btnText: 'Upload & Retrieve',
      btnClass: 'btn-saas-secondary',
      gradient: 'linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.06))',
      borderGlow: 'rgba(16,185,129,0.25)',
    },
    {
      icon: '🎯',
      title: 'Answer Evaluator',
      badge: '3-Metric Feedback',
      badgeClass: 'badge-rose',
      desc: 'Submit written answers to test your Technical accuracy, Communication structure, and Confidence scores.',
      href: '/evaluation',
      btnText: 'Evaluate Response',
      btnClass: 'btn-saas-secondary',
      gradient: 'linear-gradient(135deg, rgba(236,72,153,0.1), rgba(245,158,11,0.06))',
      borderGlow: 'rgba(236,72,153,0.25)',
    },
  ];

  const isOnline = health?.status === 'Healthy';

  return (
    <div style={{ position: 'relative', minHeight: '100vh', paddingTop: '48px', paddingBottom: '64px' }}>
      {/* Aurora background */}
      <div style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        pointerEvents: 'none',
        background: `
          radial-gradient(ellipse 50% 60% at 5% 20%, rgba(124,58,237,0.12) 0%, transparent 60%),
          radial-gradient(ellipse 40% 50% at 90% 80%, rgba(236,72,153,0.09) 0%, transparent 55%),
          radial-gradient(ellipse 60% 50% at 50% 50%, rgba(6,182,212,0.05) 0%, transparent 70%)
        `,
      }} />
      <div className="grid-texture" style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', opacity: 0.3 }} />

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>

        {/* ── HEADER ── */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          flexWrap: 'wrap',
          gap: '16px',
          marginBottom: '36px',
          paddingBottom: '28px',
          borderBottom: '1px solid var(--glass-border)',
        }}>
          <div>
            <div className="fade-in-up-1" style={{ marginBottom: '8px' }}>
              <span className="section-label">Command Center</span>
            </div>
            <h2 className="fade-in-up-2" style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.6rem, 4vw, 2.4rem)',
              fontWeight: 800,
              color: '#ffffff',
              letterSpacing: '-0.03em',
              marginBottom: '6px',
            }}>
              Welcome back,{' '}
              <span style={{
                background: 'linear-gradient(135deg, #A855F7, #EC4899)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}>
                {user?.full_name || 'Candidate'}
              </span>{' '}
              👋
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: 0, fontFamily: 'var(--font-display)' }}>
              Interview Preparation Command Center
            </p>
          </div>

          {/* Backend status pill */}
          <div className="fade-in-up-3 glass-card" style={{
            padding: '10px 20px',
            borderRadius: '999px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            border: `1px solid ${isOnline ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}`,
          }}>
            <div style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: loading ? '#F59E0B' : isOnline ? 'var(--emerald)' : 'var(--danger)',
              boxShadow: loading ? '0 0 10px rgba(245,158,11,0.5)' : isOnline ? '0 0 10px rgba(16,185,129,0.6)' : '0 0 10px rgba(239,68,68,0.5)',
              flexShrink: 0,
            }} className="pulse-dot" />
            <span style={{
              fontSize: '0.85rem',
              fontWeight: 700,
              fontFamily: 'var(--font-display)',
              color: '#ffffff',
              letterSpacing: '0.01em',
            }}>
              Backend API: {loading ? 'Checking...' : health?.status || 'Offline'}
            </span>
          </div>
        </div>

        {/* ── PREP TOPICS ── */}
        <div className="glass-card fade-in-up-2" style={{ padding: '20px 24px', marginBottom: '28px' }}>
          <div style={{
            fontSize: '0.7rem',
            fontWeight: 700,
            fontFamily: 'var(--font-display)',
            color: 'var(--text-subtle)',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            marginBottom: '14px',
          }}>
            Suggested Preparation Topics
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {categories.map((cat, i) => (
              <Link
                key={i}
                href={`/chat?topic=${encodeURIComponent(cat.label)}`}
                className="topic-chip"
                style={{
                  background: cat.color,
                  border: `1px solid ${cat.border}`,
                  color: cat.text,
                }}
              >
                {cat.label}
              </Link>
            ))}
          </div>
        </div>

        {/* ── METRICS ── */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '40px' }}>
          {metrics.map((m, i) => (
            <div key={i} className={`glass-card fade-in-up-${i + 1}`} style={{
              padding: '20px',
              position: 'relative',
              overflow: 'hidden',
              border: `1px solid rgba(255,255,255,0.07)`,
            }}>
              {/* Accent glow top-left */}
              <div style={{
                position: 'absolute',
                top: '-20px',
                right: '-20px',
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                background: `radial-gradient(circle, ${m.accent}30, transparent 70%)`,
                pointerEvents: 'none',
              }} />
              <div style={{
                fontSize: '1.5rem',
                marginBottom: '8px',
              }}>{m.icon}</div>
              <div style={{
                fontFamily: 'var(--font-display)',
                fontSize: '0.68rem',
                fontWeight: 700,
                color: 'var(--text-subtle)',
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                marginBottom: '6px',
              }}>{m.label}</div>
              <div style={{
                fontFamily: 'var(--font-display)',
                color: '#ffffff',
                fontSize: '1.05rem',
                fontWeight: 700,
                marginBottom: '4px',
                letterSpacing: '-0.01em',
              }}>{m.value}</div>
              <div style={{ color: m.subColor, fontSize: '0.75rem', fontWeight: 600, fontFamily: 'var(--font-display)' }}>
                {m.sub}
              </div>
            </div>
          ))}
        </div>

        {/* ── QUICK ACTIONS ── */}
        <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h4 style={{
            fontFamily: 'var(--font-display)',
            fontWeight: 800,
            color: '#ffffff',
            fontSize: '1.3rem',
            letterSpacing: '-0.02em',
            margin: 0,
          }}>Quick Actions</h4>
          <div style={{ flex: 1, height: '1px', background: 'linear-gradient(90deg, var(--glass-border), transparent)' }} />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '20px' }}>
          {quickActions.map((qa, i) => (
            <div key={i} className={`glass-card glass-card-glow fade-in-up-${i + 2}`} style={{
              padding: '28px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              background: `${qa.gradient}`,
              border: `1px solid ${qa.borderGlow}`,
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '16px' }}>
                  <span style={{ fontSize: '2.2rem', lineHeight: 1 }}>{qa.icon}</span>
                  <div>
                    <h5 style={{
                      fontFamily: 'var(--font-display)',
                      fontWeight: 700,
                      fontSize: '1.05rem',
                      color: '#fff',
                      margin: '0 0 6px',
                      letterSpacing: '-0.02em',
                    }}>{qa.title}</h5>
                    <span className={qa.badgeClass}>{qa.badge}</span>
                  </div>
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.65, margin: 0 }}>
                  {qa.desc}
                </p>
              </div>
              <Link href={qa.href} className={qa.btnClass} style={{ marginTop: '24px', width: '100%', justifyContent: 'center' }}>
                {qa.btnText}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
