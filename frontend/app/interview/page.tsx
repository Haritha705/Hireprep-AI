'use client';

import React, { useState } from 'react';
import { generateInterviewQuestions } from '@/lib/api';

export default function InterviewPrepPage() {
  const [skills, setSkills] = useState('');
  const [projects, setProjects] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!skills) {
      setError('Please enter at least one skill.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const res = await generateInterviewQuestions(skills, projects);
      setResult(res.data);
    } catch (err: any) {
      setError('Failed to generate interview questions.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="text-center mb-4">
        <h2 className="fw-bold gradient-text">Interview Preparation Bank</h2>
        <p style={{ color: 'var(--muted2)', fontSize: '0.9rem' }}>
          Enter your target skills and projects to retrieve customized interview questions.
        </p>
      </div>

      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="glass-card p-4 mb-4">
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label>Skills (comma separated)</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Python, FastAPI, MongoDB, LangChain, React"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                  required
                />
              </div>

              <div className="mb-3">
                <label>Projects (optional)</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="AI Resume Evaluator, RAG Chatbot"
                  value={projects}
                  onChange={(e) => setProjects(e.target.value)}
                />
              </div>

              {error && <div className="alert alert-danger py-2 px-3 mb-3">{error}</div>}

              <button
                type="submit"
                className="btn btn-neon-fill w-100 py-2 d-flex justify-content-center align-items-center gap-2"
                disabled={loading}
              >
                {loading ? <div className="spinner-sm"></div> : 'Generate Question Bank'}
              </button>
            </form>
          </div>

          {result && (
            <div className="glass-card p-4 fade-in-up">
              <div className="d-flex align-items-center justify-content-between mb-3">
                <h4 className="fw-bold gradient-text mb-0">Detected Role: {result.detected_role}</h4>
                <span className="badge-neon">MongoDB RAG Retriever</span>
              </div>

              {result.ai_interview_guide?.response && (
                <div
                  className="p-3 mb-4 text-white-50"
                  style={{
                    background: 'var(--surface)',
                    borderRadius: '10px',
                    fontSize: '0.88rem',
                    whiteSpace: 'pre-wrap',
                    lineHeight: '1.6',
                  }}
                >
                  {result.ai_interview_guide.response}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
