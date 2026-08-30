'use client';

import React, { useState } from 'react';
import { evaluateAnswer } from '@/lib/api';

export default function EvaluationPage() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [resumeContext, setResumeContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question || !answer) {
      setError('Please provide both the interview question and your written answer.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const res = await evaluateAnswer(question, answer, resumeContext);
      setResult(res.data);
    } catch (err: any) {
      setError('Evaluation failed. Please verify your backend server is active.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="text-center mb-4">
        <h2 className="fw-bold text-white mb-1">AI Answer Evaluator</h2>
        <p className="text-subtle mb-0" style={{ fontSize: '0.95rem' }}>
          Evaluate any interview question & answer against AI scoring metrics for Technical depth, Communication, and Confidence.
        </p>
      </div>

      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="saas-card p-4 mb-4">
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label>Interview Question</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. How do you optimize a slow database query in production?"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  required
                />
              </div>

              <div className="mb-3">
                <label>Your Spoken or Written Answer</label>
                <textarea
                  className="form-control"
                  rows={5}
                  placeholder="Type or paste your answer here..."
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  required
                ></textarea>
              </div>

              <div className="mb-4">
                <label>Optional Resume Context</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. Senior Backend Developer with 3 years Python/FastAPI experience"
                  value={resumeContext}
                  onChange={(e) => setResumeContext(e.target.value)}
                />
              </div>

              {error && (
                <div className="alert alert-danger py-2 px-3 mb-3" style={{ fontSize: '0.88rem', background: 'var(--danger-bg)', borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}>
                  ⚠️ {error}
                </div>
              )}

              <button
                type="submit"
                className="btn btn-saas-primary w-100 py-2 justify-content-center"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="spinner-border spinner-border-sm me-2" role="status"></div>
                    Evaluating Answer Metrics...
                  </>
                ) : (
                  '📊 Evaluate Answer'
                )}
              </button>
            </form>
          </div>

          {/* ── EVALUATION RESULT CARDS ── */}
          {result && (
            <div className="saas-card p-4">
              <h4 className="fw-bold text-white mb-4">Evaluation Scores</h4>

              <div className="row g-3 mb-4">
                <div className="col-md-3 col-6">
                  <div className="p-3 text-center rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--success)' }}>
                      {result.evaluation?.overall_score || 0}/10
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '600' }}>Overall Score</div>
                  </div>
                </div>

                <div className="col-md-3 col-6">
                  <div className="p-3 text-center rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--primary)' }}>
                      {result.evaluation?.technical_score || 0}/10
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '600' }}>Technical Depth</div>
                  </div>
                </div>

                <div className="col-md-3 col-6">
                  <div className="p-3 text-center rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--blue)' }}>
                      {result.evaluation?.communication_score || 0}/10
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '600' }}>Communication</div>
                  </div>
                </div>

                <div className="col-md-3 col-6">
                  <div className="p-3 text-center rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '2rem', fontWeight: '800', color: 'var(--violet)' }}>
                      {result.evaluation?.confidence_score || 0}/10
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: '600' }}>Confidence</div>
                  </div>
                </div>
              </div>

              {result.feedback && (
                <div>
                  <h5 className="fw-bold text-white mb-2">Detailed AI Feedback & Recommendations</h5>
                  <div
                    className="p-3 rounded"
                    style={{
                      background: 'var(--surface)',
                      border: '1px solid var(--border)',
                      fontSize: '0.92rem',
                      whiteSpace: 'pre-wrap',
                      lineHeight: '1.6',
                      color: 'var(--text-body)',
                    }}
                  >
                    {typeof result.feedback === 'object' ? JSON.stringify(result.feedback, null, 2) : result.feedback}
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
