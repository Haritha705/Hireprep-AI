'use client';

import React, { useState, useRef } from 'react';
import { startVoiceInterview, respondToInterview, getInterviewSummary } from '@/lib/api';

export default function VoiceInterviewPage() {
  const [screen, setScreen] = useState<'setup' | 'interview' | 'summary'>('setup');
  const [file, setFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Interview state
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [questionNum, setQuestionNum] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(35);
  const [aiQuestion, setAiQuestion] = useState('—');
  const [userTranscript, setUserTranscript] = useState('Press the mic button when the AI finishes speaking.');
  const [status, setStatus] = useState<'thinking' | 'speaking' | 'recording' | 'waiting'>('waiting');
  const [statusText, setStatusText] = useState('Getting ready...');
  const [lastScore, setLastScore] = useState<number | null>(null);
  const [history, setHistory] = useState<Array<{ role: 'ai' | 'user'; text: string }>>([]);

  // Recording & Audio
  const [isRecording, setIsRecording] = useState(false);
  const [canRecord, setCanRecord] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);

  // Summary state
  const [summaryData, setSummaryData] = useState<any>(null);

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !resumeText.trim()) {
      setError('Please upload a resume PDF or paste your resume text to begin.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const res = await startVoiceInterview(file, resumeText);
      const data = res.data;
      setSessionId(data.session_id);
      setQuestionNum(data.question_num);
      setTotalQuestions(data.total);
      setAiQuestion(data.question_text);
      setHistory([{ role: 'ai', text: data.question_text }]);
      setScreen('interview');

      playAiAudio(data.audio_url);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to start voice interview session.');
    } finally {
      setLoading(false);
    }
  };

  const playAiAudio = (audioUrl: string) => {
    setStatus('speaking');
    setStatusText('AI Interviewer is speaking...');
    setCanRecord(false);

    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
    }

    const fullUrl = audioUrl.startsWith('http') ? audioUrl : `http://localhost:8000${audioUrl}`;
    const audio = new Audio(fullUrl);
    currentAudioRef.current = audio;

    audio.play().catch(console.error);

    audio.onended = () => {
      setStatus('waiting');
      setStatusText('Your turn to speak');
      setCanRecord(true);
    };

    audio.onerror = () => {
      setStatus('waiting');
      setStatusText('Your turn to speak');
      setCanRecord(true);
    };
  };

  const toggleRecording = async () => {
    if (!canRecord && !isRecording) return;

    if (!isRecording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioChunksRef.current = [];
        const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorderRef.current = recorder;

        recorder.ondataavailable = (e) => audioChunksRef.current.push(e.data);
        recorder.onstop = async () => {
          stream.getTracks().forEach((t) => t.stop());
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          await handleSendAnswer(audioBlob);
        };

        recorder.start();
        setIsRecording(true);
        setStatus('recording');
        setStatusText('Recording your answer...');
        setUserTranscript('Listening to your spoken response...');
      } catch (err) {
        setError('Microphone access was denied. Please allow mic permissions in your browser.');
      }
    } else {
      setIsRecording(false);
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
      setCanRecord(false);
      setStatus('thinking');
      setStatusText('Transcribing & evaluating response...');
    }
  };

  const handleSendAnswer = async (audioBlob: Blob) => {
    if (!sessionId) return;

    try {
      const res = await respondToInterview(sessionId, audioBlob);
      const data = res.data;

      setUserTranscript(data.transcript || '(no speech detected)');
      setHistory((prev) => [
        ...prev,
        { role: 'user', text: data.transcript || '' },
        { role: 'ai', text: data.feedback || '' },
      ]);

      if (data.score !== null && data.score !== undefined) {
        setLastScore(data.score);
      }

      if (data.done) {
        playAiAudio(data.audio_url);
        fetchSummary(sessionId);
        return;
      }

      setQuestionNum(data.question_num);
      setAiQuestion(data.feedback);
      playAiAudio(data.audio_url);
    } catch (err: any) {
      setError('Error processing your audio response.');
      setStatus('waiting');
      setCanRecord(true);
    }
  };

  const fetchSummary = async (sId: string) => {
    try {
      const res = await getInterviewSummary(sId);
      setSummaryData(res.data);
      setScreen('summary');
    } catch (err) {
      setError('Could not fetch session summary.');
    }
  };

  const getSectionLabel = () => {
    if (questionNum <= 15) return 'Stage 1: Technical & Systems';
    if (questionNum <= 25) return 'Stage 2: Project Architecture';
    return 'Stage 3: HR & Behavioral';
  };

  return (
    <div className="container py-5">
      {/* ── SETUP SCREEN ── */}
      {screen === 'setup' && (
        <div className="row justify-content-center">
          <div className="col-lg-7">
            <div className="saas-card p-4 p-md-5">
              <div className="text-center mb-4">
                <span style={{ fontSize: '3rem' }}>🎙️</span>
                <h2 className="fw-bold text-white mt-2 mb-1">Real-Time AI Voice Interview</h2>
                <p className="text-subtle mb-0" style={{ fontSize: '0.92rem' }}>
                  Upload your resume PDF or paste plain text to launch a 35-question live voice interview session.
                </p>
              </div>

              {error && (
                <div className="alert alert-danger py-2 px-3 mb-3" style={{ fontSize: '0.88rem', background: 'var(--danger-bg)', borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}>
                  ⚠️ {error}
                </div>
              )}

              <form onSubmit={handleStart}>
                <div className="mb-3">
                  <label>Option A: Upload Resume PDF</label>
                  <input
                    type="file"
                    className="form-control"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                  />
                  {file && <div className="mt-1 text-success fw-bold" style={{ fontSize: '0.82rem' }}>✔ Selected: {file.name}</div>}
                </div>

                <div className="text-center my-3 fw-bold" style={{ color: 'var(--text-subtle)', fontSize: '0.8rem' }}>OR</div>

                <div className="mb-4">
                  <label>Option B: Paste Resume Plain Text</label>
                  <textarea
                    className="form-control"
                    rows={4}
                    placeholder="Paste skills, past projects, or experience here..."
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                  ></textarea>
                </div>

                <div className="p-3 mb-4 rounded" style={{ background: 'var(--surface)', border: '1px solid var(--border)', fontSize: '0.85rem' }}>
                  <strong style={{ color: 'var(--primary)' }}>Structured 35-Question Assessment:</strong>
                  <ul className="mb-0 mt-1 ps-3 text-subtle">
                    <li>15 Technical & System Architecture Questions</li>
                    <li>10 Project Deep-Dive & Decision Questions</li>
                    <li>10 HR, Behavioral & Cultural Questions</li>
                  </ul>
                </div>

                <button
                  type="submit"
                  className="btn btn-saas-primary w-100 py-3 justify-content-center"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <div className="spinner-border spinner-border-sm me-2" role="status"></div>
                      Initializing Voice Interview Session...
                    </>
                  ) : (
                    '🎙️ Start AI Voice Interview'
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* ── INTERVIEW SCREEN ── */}
      {screen === 'interview' && (
        <div className="row justify-content-center">
          <div className="col-lg-8">
            {/* Progress Header */}
            <div className="mb-4">
              <div className="d-flex justify-content-between align-items-center mb-2" style={{ fontSize: '0.88rem' }}>
                <span className="fw-bold text-white">Question {questionNum} of {totalQuestions}</span>
                <span className="badge-indigo">{getSectionLabel()}</span>
              </div>
              <div className="progress">
                <div
                  className="progress-bar"
                  style={{ width: `${Math.round((questionNum / totalQuestions) * 100)}%` }}
                ></div>
              </div>
            </div>

            {/* AI Avatar */}
            <div className="text-center my-4">
              <div
                className="mx-auto rounded-circle d-flex align-items-center justify-content-center mb-2"
                style={{
                  width: '100px',
                  height: '100px',
                  backgroundColor: 'var(--surface)',
                  border: `3px solid ${status === 'recording' ? 'var(--danger)' : 'var(--primary)'}`,
                  fontSize: '2.5rem',
                }}
              >
                🤖
              </div>
              <div>
                <span className={status === 'recording' ? 'badge-amber' : 'badge-indigo'} style={{ fontSize: '0.85rem', padding: '6px 16px' }}>
                  {statusText}
                </span>
              </div>
            </div>

            {/* AI Question Box */}
            <div className="saas-card p-4 mb-3">
              <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.08em' }} className="mb-2">
                AI Interviewer Question
              </div>
              <div style={{ fontSize: '1.1rem', color: '#ffffff', lineHeight: '1.6', fontWeight: '600' }}>
                {aiQuestion}
              </div>
            </div>

            {/* Score pill */}
            {lastScore !== null && (
              <div className="d-flex align-items-center gap-2 mb-3">
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Last Answer Score:</span>
                <span className="badge-emerald">{lastScore} / 10 Points</span>
              </div>
            )}

            {/* User Transcript Box */}
            <div className="saas-card p-4 mb-4">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--violet)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                  Your Spoken Response
                </div>
                {isRecording && (
                  <div className="waveform">
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                  </div>
                )}
              </div>
              <div style={{ fontSize: '0.95rem', color: 'var(--text-body)', lineHeight: '1.6' }}>
                {userTranscript}
              </div>
            </div>

            {/* Mic Controls */}
            <div className="text-center mb-4">
              <button
                className={`btn ${isRecording ? 'btn-danger' : 'btn-saas-primary'} rounded-circle p-4`}
                style={{ width: '80px', height: '80px', fontSize: '1.8rem', border: 'none' }}
                onClick={toggleRecording}
                disabled={!canRecord && !isRecording}
              >
                {isRecording ? '⏹️' : '🎙️'}
              </button>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '12px' }}>
                {isRecording ? 'Click to stop & evaluate answer' : canRecord ? 'Click mic to record your answer' : 'Listening to AI interviewer...'}
              </div>
            </div>

            {/* Conversation Log */}
            <div className="saas-card p-3">
              <div style={{ fontSize: '0.78rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }} className="mb-2">
                Live Conversation Log
              </div>
              <div className="d-flex flex-column gap-2" style={{ maxHeight: '180px', overflowY: 'auto' }}>
                {history.map((h, i) => (
                  <div key={i} className="p-2 rounded" style={{ background: 'var(--surface)', fontSize: '0.85rem' }}>
                    <strong style={{ color: h.role === 'ai' ? 'var(--primary)' : 'var(--violet)' }}>
                      {h.role === 'ai' ? 'AI: ' : 'You: '}
                    </strong>
                    <span style={{ color: 'var(--text-body)' }}>{h.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── SUMMARY SCREEN ── */}
      {screen === 'summary' && summaryData && (
        <div className="row justify-content-center">
          <div className="col-lg-7 text-center">
            <div className="saas-card p-5">
              <span style={{ fontSize: '3.5rem' }}>🎉</span>
              <h2 className="fw-bold text-white mt-3 mb-1">Interview Completed!</h2>
              <p className="text-subtle mb-4">You completed your live AI voice interview assessment.</p>

              <div className="my-4">
                <div
                  className="mx-auto rounded-circle d-flex flex-column align-items-center justify-content-center"
                  style={{
                    width: '140px',
                    height: '140px',
                    border: '4px solid var(--primary)',
                    background: 'var(--surface)',
                  }}
                >
                  <div style={{ fontSize: '2.2rem', fontWeight: '800', color: '#ffffff' }}>
                    {summaryData.average_score}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Average / 10</div>
                </div>
              </div>

              <div className="d-flex justify-content-center gap-4 mb-4">
                <div>
                  <div className="fw-bold fs-4 text-white">{summaryData.answered}</div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Questions Answered</div>
                </div>
                <div>
                  <div className="fw-bold fs-4 text-white">{summaryData.total_questions}</div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Total Target</div>
                </div>
              </div>

              <button className="btn btn-saas-primary px-4 py-2" onClick={() => setScreen('setup')}>
                🔄 Start New Interview Session
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
