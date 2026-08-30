'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  const workflowSteps = [
    { num: '01', title: 'Upload Resume', desc: 'PDF parsing extracts skills, projects & detected role.', color: 'violet' },
    { num: '02', title: 'Analyze Role', desc: 'Classifies candidate profile & technical level.', color: 'rose' },
    { num: '03', title: 'Retrieve RAG', desc: 'Queries MongoDB Vector DB for tailored questions.', color: 'cyan' },
    { num: '04', title: 'Personalize', desc: 'Gemini creates customized interview prep guides.', color: 'emerald' },
    { num: '05', title: 'Voice Practice', desc: 'Live STT & TTS mock interview sessions.', color: 'gold' },
    { num: '06', title: 'AI Scoring', desc: 'Instant evaluation on technical, voice & confidence.', color: 'violet' },
  ];

  const features = [
    {
      icon: '📄',
      iconClass: 'icon-orb-violet',
      title: 'Resume-Based Questions',
      desc: 'Automatically parses your PDF resume to extract projects, tech stack, and key skills to build targeted question banks.',
      href: '/upload',
      badge: 'PDF Parser',
      badgeClass: 'badge-indigo',
      gradient: 'from-violet to-primary',
    },
    {
      icon: '⚡',
      iconClass: 'icon-orb-cyan',
      title: 'AI-Powered RAG',
      desc: '768-dimensional vector embeddings retrieve the exact technical, project, and HR questions matching your candidate profile.',
      href: '/upload',
      badge: 'Vector DB RAG',
      badgeClass: 'badge-cyan',
    },
    {
      icon: '🎯',
      iconClass: 'icon-orb-emerald',
      title: 'Role-Specific Preparation',
      desc: 'Tailored questions and guidance for Full Stack Developers, Data Analysts, Generative AI Engineers, and Software Engineers.',
      href: '/upload',
      badge: 'Role Classifier',
      badgeClass: 'badge-emerald',
    },
    {
      icon: '🐍',
      iconClass: 'icon-orb-rose',
      title: 'Python & SQL Practice',
      desc: 'Practice core algorithmic logic, data manipulations, SQL queries, and system design problems frequently asked in tech interviews.',
      href: '/chat',
      badge: 'Coding Practice',
      badgeClass: 'badge-rose',
    },
    {
      icon: '🤖',
      iconClass: 'icon-orb-gold',
      title: 'Generative AI Preparation',
      desc: 'Master modern AI concepts including RAG architectures, LLM fine-tuning, prompt engineering, and vector databases.',
      href: '/chat',
      badge: 'GenAI & LLMs',
      badgeClass: 'badge-gold',
    },
    {
      icon: '🎙️',
      iconClass: 'icon-orb-violet',
      title: 'Personalized Mock Interviews',
      desc: 'Real-time 35-question live voice interview with Groq Whisper STT transcription and Edge-TTS audio playback.',
      href: '/voice-interview',
      badge: 'Live Voice AI',
      badgeClass: 'badge-indigo',
    },
  ];

  const stats = [
    { value: '35+', label: 'Live Questions', color: 'var(--violet-light)' },
    { value: '4', label: 'Role Profiles', color: 'var(--rose)' },
    { value: '768D', label: 'Vector Embeddings', color: 'var(--cyan)' },
    { value: '3x', label: 'Evaluation Metrics', color: '#F59E0B' },
  ];

  return (
    <div style={{ position: 'relative', overflow: 'hidden' }}>
      {/* Aurora background mesh */}
      <div style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        pointerEvents: 'none',
        background: `
          radial-gradient(ellipse 60% 50% at 15% 25%, rgba(124,58,237,0.18) 0%, transparent 65%),
          radial-gradient(ellipse 50% 45% at 75% 10%, rgba(236,72,153,0.12) 0%, transparent 60%),
          radial-gradient(ellipse 70% 55% at 55% 85%, rgba(6,182,212,0.09) 0%, transparent 65%),
          radial-gradient(ellipse 45% 50% at 25% 75%, rgba(139,92,246,0.1) 0%, transparent 55%)
        `,
      }} />

      {/* Grid texture */}
      <div className="grid-texture" style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        pointerEvents: 'none',
        opacity: 0.4,
      }} />

      {/* ── HERO ── */}
      <section style={{ position: 'relative', zIndex: 1, padding: '100px 0 80px' }}>
        {/* Floating orbs */}
        <div className="orb orb-violet" style={{ width: '500px', height: '500px', top: '-150px', left: '-100px', opacity: 0.2 }} />
        <div className="orb orb-rose" style={{ width: '400px', height: '400px', top: '-50px', right: '-120px', opacity: 0.15 }} />
        <div className="orb orb-cyan" style={{ width: '300px', height: '300px', bottom: '-80px', left: '40%', opacity: 0.1 }} />

        <div className="container" style={{ textAlign: 'center', position: 'relative' }}>
          {/* Eyebrow label */}
          <div className={`fade-in-up-1${mounted ? '' : ''}`} style={{ marginBottom: '24px' }}>
            <span className="section-label">
              <span style={{
                display: 'inline-block',
                width: '7px', height: '7px',
                borderRadius: '50%',
                background: 'var(--violet-light)',
                marginRight: '8px',
                verticalAlign: 'middle',
              }} className="pulse-dot" />
              Enterprise AI Interview Preparation Platform
            </span>
          </div>

          {/* Main heading */}
          <h1 className="fade-in-up-2" style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2.8rem, 7vw, 5.5rem)',
            fontWeight: 900,
            lineHeight: 1.08,
            letterSpacing: '-0.04em',
            marginBottom: '28px',
            color: '#ffffff',
          }}>
            Prepare Smarter.{' '}
            <span className="shimmer-text">Interview Better.</span>
          </h1>

          {/* Subheading */}
          <p className="fade-in-up-3" style={{
            maxWidth: '640px',
            margin: '0 auto 44px',
            fontSize: '1.15rem',
            lineHeight: 1.75,
            color: 'var(--text-muted)',
          }}>
            HirePrep AI uses your resume, Gemini AI, and MongoDB Vector RAG retrieval to generate
            role-tailored questions, real-time voice interviews, and instant performance scoring.
          </p>

          {/* CTA Buttons */}
          <div className="fade-in-up-4" style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '72px' }}>
            <Link href="/voice-interview" className="btn-luxury-primary glow-pulse">
              🎙️ Start Preparing
            </Link>
            <Link href="/upload" className="btn-luxury-glass">
              📄 Upload Resume
            </Link>
          </div>

          {/* Stats Row */}
          <div className="fade-in-up-5" style={{
            display: 'flex',
            gap: '0',
            justifyContent: 'center',
            flexWrap: 'wrap',
          }}>
            <div className="glass-card" style={{
              display: 'inline-flex',
              gap: '0',
              borderRadius: '20px',
              overflow: 'hidden',
              padding: '0',
            }}>
              {stats.map((s, i) => (
                <div key={i} style={{
                  padding: '20px 36px',
                  textAlign: 'center',
                  borderRight: i < stats.length - 1 ? '1px solid var(--glass-border)' : 'none',
                }}>
                  <div style={{
                    fontSize: '1.8rem',
                    fontWeight: 800,
                    fontFamily: 'var(--font-display)',
                    color: s.color,
                    letterSpacing: '-0.03em',
                    lineHeight: 1,
                    marginBottom: '4px',
                  }}>{s.value}</div>
                  <div style={{ fontSize: '0.76rem', color: 'var(--text-subtle)', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                    {s.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── WORKFLOW SECTION ── */}
      <section style={{ position: 'relative', zIndex: 1, padding: '80px 0' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            <span className="section-label" style={{ marginBottom: '20px', display: 'inline-block' }}>How It Works</span>
            <h2 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.8rem, 4vw, 2.8rem)',
              fontWeight: 800,
              color: '#fff',
              marginBottom: '12px',
            }}>
              Clean End-to-End Workflow
            </h2>
            <p style={{ color: 'var(--text-muted)', maxWidth: '500px', margin: '0 auto', fontSize: '1rem' }}>
              How HirePrep AI transforms your resume into an interactive practice session
            </p>
            <div className="glow-line" style={{ marginTop: '24px' }} />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '16px' }}>
            {workflowSteps.map((s, idx) => (
              <div key={idx} className={`glass-card glass-card-glow fade-in-up-${Math.min(idx + 1, 6)}`}
                style={{ padding: '24px 20px', textAlign: 'center', cursor: 'default' }}>
                <div className="step-num" style={{ margin: '0 auto 16px' }}>{s.num}</div>
                <div style={{ fontFamily: 'var(--font-display)', color: '#ffffff', fontWeight: 700, fontSize: '0.92rem', marginBottom: '8px' }}>
                  {s.title}
                </div>
                <div style={{ color: 'var(--text-subtle)', fontSize: '0.78rem', lineHeight: 1.5 }}>
                  {s.desc}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES SECTION ── */}
      <section style={{ position: 'relative', zIndex: 1, padding: '80px 0 100px' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            <span className="section-label" style={{ marginBottom: '20px', display: 'inline-block' }}>Feature Suite</span>
            <h2 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(1.8rem, 4vw, 2.8rem)',
              fontWeight: 800,
              color: '#fff',
              marginBottom: '12px',
            }}>
              Comprehensive Interview Suite
            </h2>
            <p style={{ color: 'var(--text-muted)', maxWidth: '520px', margin: '0 auto', fontSize: '1rem' }}>
              Everything required to excel in modern technical, behavioral, and system design interviews
            </p>
            <div className="glow-line" style={{ marginTop: '24px' }} />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
            {features.map((f, idx) => (
              <div key={idx} className={`glass-card glass-card-glow fade-in-up-${Math.min(idx + 1, 6)}`}
                style={{ padding: '28px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
                    <div className={`icon-orb ${f.iconClass}`}>
                      {f.icon}
                    </div>
                    <span className={f.badgeClass}>{f.badge}</span>
                  </div>
                  <h5 style={{
                    fontFamily: 'var(--font-display)',
                    fontWeight: 700,
                    fontSize: '1.1rem',
                    color: '#fff',
                    marginBottom: '12px',
                    letterSpacing: '-0.02em',
                  }}>{f.title}</h5>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.65 }}>{f.desc}</p>
                </div>
                <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid var(--glass-border)' }}>
                  <Link href={f.href} className="btn-saas-outline" style={{ width: '100%', justifyContent: 'center' }}>
                    Launch Feature →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
