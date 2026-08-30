'use client';

import Link from 'next/link';

export default function Footer() {
  return (
    <footer style={{
      position: 'relative',
      borderTop: '1px solid rgba(255,255,255,0.07)',
      background: 'rgba(3,1,10,0.8)',
      backdropFilter: 'blur(20px)',
      padding: '56px 0 28px',
      marginTop: 'auto',
      overflow: 'hidden',
    }}>
      {/* Subtle aurora glow at top */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '600px',
        height: '1px',
        background: 'linear-gradient(90deg, transparent, rgba(139,92,246,0.5), rgba(236,72,153,0.4), transparent)',
        pointerEvents: 'none',
      }} />
      <div style={{
        position: 'absolute',
        top: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '400px',
        height: '80px',
        background: 'radial-gradient(ellipse 70% 100% at 50% 0%, rgba(139,92,246,0.08), transparent)',
        pointerEvents: 'none',
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '40px', marginBottom: '48px' }}>
          
          {/* Brand */}
          <div style={{ gridColumn: 'span 1' }}>
            <Link href="/" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '9px',
                background: 'linear-gradient(135deg, #7C3AED, #EC4899)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontFamily: 'var(--font-display)',
                fontWeight: 900,
                fontSize: '1rem',
                boxShadow: '0 4px 16px rgba(124,58,237,0.35)',
              }}>H</div>
              <span style={{
                fontFamily: 'var(--font-display)',
                fontWeight: 800,
                fontSize: '1.15rem',
                letterSpacing: '-0.03em',
                color: '#fff',
              }}>
                HirePrep{' '}
                <span style={{
                  background: 'linear-gradient(135deg, #A855F7, #EC4899)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                }}>AI</span>
              </span>
            </Link>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.7, maxWidth: '280px' }}>
              Autonomous AI Resume Analysis, Vector RAG Question Retrieval, Real-Time Voice Interviewer & Performance Evaluator.
            </p>
          </div>

          {/* Platform Tools */}
          <div>
            <h6 style={{
              fontFamily: 'var(--font-display)',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: 'var(--text-subtle)',
              marginBottom: '16px',
            }}>Platform Tools</h6>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {[
                { label: 'AI Voice Interviewer', href: '/voice-interview' },
                { label: 'Resume Parser & RAG', href: '/upload' },
                { label: 'Answer Evaluator', href: '/evaluation' },
                { label: 'AI Assistant Chat', href: '/chat' },
              ].map((l) => (
                <li key={l.href}>
                  <Link href={l.href} className="footer-nav-link">
                    <span style={{ color: 'var(--violet-light)', fontSize: '0.6rem' }}>◆</span>
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Backend Status */}
          <div>
            <h6 style={{
              fontFamily: 'var(--font-display)',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: 'var(--text-subtle)',
              marginBottom: '16px',
            }}>Backend Architecture</h6>
            <div className="glass-card" style={{ padding: '16px 18px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '10px',
                  height: '10px',
                  borderRadius: '50%',
                  background: 'var(--emerald)',
                  flexShrink: 0,
                  boxShadow: '0 0 10px rgba(16,185,129,0.6)',
                }} className="pulse-dot" />
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: 700, fontFamily: 'var(--font-display)', color: '#ffffff' }}>
                    FastAPI & MongoDB Connected
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    Vector Search + Groq Whisper STT + Edge-TTS
                  </div>
                </div>
              </div>
            </div>

            {/* Tech chips */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '14px' }}>
              {['Gemini 2.5', 'Groq Llama', 'MongoDB', 'FastAPI'].map((t) => (
                <span key={t} style={{
                  fontSize: '0.7rem',
                  fontWeight: 600,
                  fontFamily: 'var(--font-display)',
                  color: 'var(--text-subtle)',
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '999px',
                  padding: '3px 10px',
                  letterSpacing: '0.04em',
                }}>
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Divider */}
        <div style={{
          height: '1px',
          background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent)',
          marginBottom: '24px',
        }} />

        {/* Bottom row */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-subtle)', fontFamily: 'var(--font-display)' }}>
            © 2026 HirePrep AI. All rights reserved.
          </div>
          <div style={{
            fontSize: '0.8rem',
            color: 'var(--text-subtle)',
            fontFamily: 'var(--font-display)',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}>
            Powered by{' '}
            <span style={{
              background: 'linear-gradient(135deg, #A855F7, #EC4899)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              fontWeight: 700,
            }}>
              Google Gemini 2.5
            </span>
            {' '}&{' '}
            <span style={{ color: '#F59E0B', fontWeight: 700 }}>Groq Llama 3.3</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
