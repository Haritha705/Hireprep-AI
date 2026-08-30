'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { uploadResume } from '@/lib/api';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<'idle' | 'uploading' | 'parsing' | 'analyzing' | 'ready'>('idle');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a valid PDF file first.');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);

    setStep('uploading');
    setTimeout(() => setStep('parsing'), 600);
    setTimeout(() => setStep('analyzing'), 1200);

    try {
      const res = await uploadResume(file);
      setResult(res.data);
      setStep('ready');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Resume processing failed. Please check file format.');
      setStep('idle');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="text-center mb-4">
        <h2 className="fw-bold text-white mb-1">Resume Parser & RAG Question Retrieval</h2>
        <p className="text-subtle mb-0" style={{ fontSize: '0.95rem' }}>
          Upload your resume PDF to extract skills, detect candidate role, and retrieve targeted interview questions from your MongoDB Vector DB.
        </p>
      </div>

      <div className="row justify-content-center">
        <div className="col-lg-8">

          {/* ── PROGRESS FLOW BAR ── */}
          <div className="saas-card p-3 mb-4">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 text-center" style={{ fontSize: '0.85rem' }}>
              <div className={`fw-bold ${step === 'uploading' ? 'text-primary' : step === 'parsing' || step === 'analyzing' || step === 'ready' ? 'text-success' : 'text-subtle'}`}>
                1. Uploading
              </div>
              <div style={{ color: 'var(--border)' }}>→</div>
              <div className={`fw-bold ${step === 'parsing' ? 'text-primary' : step === 'analyzing' || step === 'ready' ? 'text-success' : 'text-subtle'}`}>
                2. Parsing PDF
              </div>
              <div style={{ color: 'var(--border)' }}>→</div>
              <div className={`fw-bold ${step === 'analyzing' ? 'text-primary' : step === 'ready' ? 'text-success' : 'text-subtle'}`}>
                3. Vector RAG Search
              </div>
              <div style={{ color: 'var(--border)' }}>→</div>
              <div className={`fw-bold ${step === 'ready' ? 'text-success' : 'text-subtle'}`}>
                4. Ready
              </div>
            </div>
          </div>

          {/* ── UPLOAD DRAG & DROP CARD ── */}
          <div className="saas-card p-4 mb-4 text-center">
            <form onSubmit={handleSubmit}>
              <div
                className="p-4 rounded-3 mb-3 d-flex flex-column align-items-center justify-content-center"
                style={{
                  border: '2px dashed var(--border-active)',
                  backgroundColor: 'var(--bg-subtle)',
                  cursor: 'pointer',
                }}
                onClick={() => document.getElementById('resumeFileInput')?.click()}
              >
                <div style={{ fontSize: '2.5rem' }} className="mb-2">📄</div>
                <h5 className="fw-bold text-white mb-1">Upload your resume</h5>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }} className="mb-2">
                  Drag and drop your resume file here or click to browse
                </p>
                <span className="badge-slate" style={{ fontSize: '0.78rem' }}>PDF files only</span>

                <input
                  id="resumeFileInput"
                  type="file"
                  className="d-none"
                  accept=".pdf"
                  onChange={handleFileChange}
                />
              </div>

              {file && (
                <div className="p-3 rounded mb-3 d-flex align-items-center justify-content-between" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)' }}>
                  <div className="d-flex align-items-center gap-2">
                    <span style={{ fontSize: '1.2rem' }}>📎</span>
                    <div className="text-start">
                      <div style={{ fontWeight: '700', color: '#ffffff', fontSize: '0.9rem' }}>{file.name}</div>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>{(file.size / 1024).toFixed(1)} KB</div>
                    </div>
                  </div>
                  <span className="badge-emerald">Selected</span>
                </div>
              )}

              {error && (
                <div className="alert alert-danger py-2 px-3 mb-3 text-start" style={{ fontSize: '0.88rem', background: 'var(--danger-bg)', borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}>
                  ⚠️ {error}
                </div>
              )}

              <button
                type="submit"
                className="btn btn-saas-primary w-100 py-2 justify-content-center"
                disabled={loading || !file}
              >
                {loading ? (
                  <>
                    <div className="spinner-border spinner-border-sm me-2" role="status"></div>
                    {step === 'uploading' && 'Uploading Resume...'}
                    {step === 'parsing' && 'Extracting PDF Text & Skills...'}
                    {step === 'analyzing' && 'Retrieving MongoDB Vector Questions...'}
                    {step === 'ready' && 'Finalizing Guide...'}
                  </>
                ) : (
                  'Analyze Resume & Retrieve RAG Questions'
                )}
              </button>
            </form>
          </div>

          {/* ── ANALYSIS & RETRIEVAL RESULTS ── */}
          {result && (
            <div className="saas-card p-4">
              <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2 pb-3 border-bottom" style={{ borderColor: 'var(--border)' }}>
                <div>
                  <h4 className="fw-bold text-white mb-0">Analysis & Retrieval Complete</h4>
                  <span style={{ color: 'var(--success)', fontSize: '0.85rem' }}>✔ {result.filename || 'Resume'} processed successfully</span>
                </div>
                <Link href="/voice-interview" className="btn btn-saas-primary">
                  🎙️ Start Voice Interview →
                </Link>
              </div>

              {/* Candidate Profile Metadata */}
              <div className="row g-3 mb-4">
                <div className="col-md-6">
                  <div className="p-3 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: '700' }}>DETECTED CANDIDATE ROLE</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: '800', color: '#ffffff' }} className="mt-1">
                      {result.questions?.detected_role || 'General Software Candidate'}
                    </div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="p-3 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: '700' }}>EXTRACTED SKILLS</div>
                    <div className="d-flex flex-wrap gap-1 mt-2">
                      {(result.resume?.skills || []).length > 0 ? (
                        (result.resume?.skills || []).map((s: string, i: number) => (
                          <span key={i} className="badge-indigo" style={{ fontSize: '0.78rem' }}>{s}</span>
                        ))
                      ) : (
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Full Stack & Problem Solving</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Retrieved Questions Section */}
              <div className="mb-4">
                <div className="d-flex align-items-center justify-content-between mb-3">
                  <h5 className="fw-bold text-white mb-0">📚 Retrieved Questions from Vector DB Knowledge Base</h5>
                  <span className="badge-emerald">MongoDB Vector Search</span>
                </div>

                {/* Technical Questions */}
                <div className="p-3 mb-3 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                  <div className="fw-bold mb-2" style={{ color: '#a5b4fc', fontSize: '0.92rem' }}>
                    🛠️ Technical Questions ({result.questions?.technical_questions?.length || 0})
                  </div>
                  {result.questions?.technical_questions && result.questions.technical_questions.length > 0 ? (
                    <ol className="mb-0 ps-3" style={{ fontSize: '0.9rem', color: 'var(--text-body)', lineHeight: '1.6' }}>
                      {result.questions.technical_questions.map((q: any, i: number) => (
                        <li key={i} className="mb-2">{typeof q === 'string' ? q : q.text || JSON.stringify(q)}</li>
                      ))}
                    </ol>
                  ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No technical questions retrieved.</div>
                  )}
                </div>

                {/* Project Questions */}
                <div className="p-3 mb-3 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                  <div className="fw-bold mb-2" style={{ color: '#c084fc', fontSize: '0.92rem' }}>
                    💼 Project Deep-Dive Questions ({result.questions?.project_questions?.length || 0})
                  </div>
                  {result.questions?.project_questions && result.questions.project_questions.length > 0 ? (
                    <ol className="mb-0 ps-3" style={{ fontSize: '0.9rem', color: 'var(--text-body)', lineHeight: '1.6' }}>
                      {result.questions.project_questions.map((q: any, i: number) => (
                        <li key={i} className="mb-2">{typeof q === 'string' ? q : q.text || JSON.stringify(q)}</li>
                      ))}
                    </ol>
                  ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No project questions retrieved.</div>
                  )}
                </div>

                {/* HR Questions */}
                <div className="p-3 mb-3 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                  <div className="fw-bold mb-2" style={{ color: '#fcd34d', fontSize: '0.92rem' }}>
                    👥 HR & Behavioral Questions ({result.questions?.hr_questions?.length || 0})
                  </div>
                  {result.questions?.hr_questions && result.questions.hr_questions.length > 0 ? (
                    <ol className="mb-0 ps-3" style={{ fontSize: '0.9rem', color: 'var(--text-body)', lineHeight: '1.6' }}>
                      {result.questions.hr_questions.map((q: any, i: number) => (
                        <li key={i} className="mb-2">{typeof q === 'string' ? q : q.text || JSON.stringify(q)}</li>
                      ))}
                    </ol>
                  ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No HR questions retrieved.</div>
                  )}
                </div>
              </div>

              {/* Gemini Preparation Guide */}
              {result.questions?.ai_interview_guide?.response && (
                <div>
                  <h5 className="fw-bold text-white mb-2">🤖 Gemini Interview Preparation Guide</h5>
                  <div
                    className="p-3 rounded"
                    style={{
                      background: 'var(--surface)',
                      border: '1px solid var(--border)',
                      fontSize: '0.9rem',
                      whiteSpace: 'pre-wrap',
                      lineHeight: '1.6',
                      color: 'var(--text-body)',
                    }}
                  >
                    {result.questions.ai_interview_guide.response}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
