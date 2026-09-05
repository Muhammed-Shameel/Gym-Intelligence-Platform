import { useEffect } from "react";

interface ShowcasePageProps {
  onOpenConsole: () => void;
  onOpenDashboard: () => void;
}

export function ShowcasePage({ onOpenConsole, onOpenDashboard }: ShowcasePageProps) {
  useEffect(() => {
    document.title = "Infocreon Internship | GFIP Agentic AI MVP Showcase";
  }, []);

  return (
    <div className="showcase-container" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* Hero Section */}
      <section className="hero-card" style={{ background: '#0f172a', color: '#ffffff', border: 'none', padding: '36px 32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
          <div>
            <span style={{ background: '#2563eb', color: '#ffffff', fontSize: '0.75rem', padding: '4px 12px', borderRadius: '12px', fontWeight: '700', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              INFOCREON INTERNSHIP SHOWCASE
            </span>
            <h1 style={{ fontSize: '2.2rem', margin: '12px 0 6px 0', fontWeight: '800', letterSpacing: '-0.02em', color: '#ffffff' }}>
              Gym Fitness Member Engagement & Intervention Platform (GFIP)
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '1rem', margin: 0 }}>
              Explainable workflow intelligence built through staged Agentic AI learning.
            </p>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.06)', border: '1px solid rgba(255, 255, 255, 0.12)', padding: '14px 20px', borderRadius: '12px', textAlign: 'right' }}>
            <span style={{ display: 'block', fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Built By</span>
            <strong style={{ fontSize: '1.1rem', color: '#ffffff' }}>Muhammed Shameel</strong>
            <span style={{ display: 'block', fontSize: '0.8rem', color: '#38bdf8' }}>Agentic AI Intern</span>
          </div>
        </div>

        <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button 
            onClick={onOpenConsole} 
            style={{ background: '#2563eb', color: '#ffffff', padding: '10px 20px', borderRadius: '8px', border: 'none', fontWeight: '600', cursor: 'pointer', fontSize: '0.9rem' }}
          >
            Open Agent Workflow Console
          </button>
          <button 
            onClick={onOpenDashboard} 
            style={{ background: 'rgba(255, 255, 255, 0.1)', color: '#ffffff', padding: '10px 20px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.2)', fontWeight: '600', cursor: 'pointer', fontSize: '0.9rem' }}
          >
            View Dashboard & Members
          </button>
        </div>
      </section>

      {/* Project Overview & Problem Statement */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
        <section className="panel" style={{ margin: 0 }}>
          <span className="eyebrow" style={{ color: '#2563eb' }}>Project Overview</span>
          <h2 style={{ fontSize: '1.25rem', margin: '8px 0 12px 0' }}>Domain & Application Purpose</h2>
          <p style={{ fontSize: '0.9rem', color: '#334155', lineHeight: '1.6', margin: 0 }}>
            This project is an Agentic AI MVP built as part of the Infocreon Internship.
            It provides automated decision support for gym operators and personal trainers by processing raw member check-in history,
            detecting retention risks, allocating trainer interventions, and generating human-readable narrative explanations.
          </p>
        </section>

        <section className="panel" style={{ margin: 0 }}>
          <span className="eyebrow" style={{ color: '#0284c7' }}>Problem Statement</span>
          <h2 style={{ fontSize: '1.25rem', margin: '8px 0 12px 0' }}>Fitness Member Retention Challenge</h2>
          <p style={{ fontSize: '0.9rem', color: '#334155', lineHeight: '1.6', margin: 0 }}>
            Fitness center operators face significant member churn due to unmonitored attendance drop-offs and delayed outreach.
            GFIP solves this by establishing a transparent multi-agent decision support pipeline that moves from raw attendance metrics
            to actionable, audited recommendations.
          </p>
        </section>
      </div>

      {/* Stage-wise Learning Journey */}
      <section className="panel">
        <span className="eyebrow" style={{ color: '#2563eb' }}>Internship Progression</span>
        <h2 style={{ fontSize: '1.3rem', margin: '6px 0 16px 0' }}>Stage-wise Learning Journey</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem', textAlign: 'left' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0' }}>
                <th style={{ padding: '10px 14px', color: '#475569' }}>Stage</th>
                <th style={{ padding: '10px 14px', color: '#475569' }}>What I Built</th>
                <th style={{ padding: '10px 14px', color: '#475569' }}>What I Learned</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#0f172a' }}>Stage 1</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>Deterministic workflow and agents (`AttendanceAgent`, `TrainerAllocationAgent`)</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>Business rules, shared context (`SharedWorkflowContext`), structured outputs, and audit logs</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#0f172a' }}>Stage 1.5</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>Agent Workflow Console (React Visualizer)</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>How to make agent sequence execution, context state, and audit tokens visible</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#0f172a' }}>Stage 2</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>Cloud readiness & containerization (Docker & Cloud Build)</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>Multi-environment configuration, secret handling via environment variables, and public deployment</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#0f172a' }}>Stage 3 & 3.1</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>LangGraph StateGraph & Conditional Routing (`router_node`)</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>Graph state management, conditional route execution (dormant/high-risk), and skipping redundant agents</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#0f172a' }}>Stage 4</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>LLM Agent Integration (`ExplanationSummaryService`)</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>Provider adapters (Mock/Gemini), prompt contracts, Pydantic schema validation, and deterministic fallbacks</td>
              </tr>
              <tr>
                <td style={{ padding: '12px 14px', fontWeight: 'bold', color: '#2563eb' }}>Stage 5</td>
                <td style={{ padding: '12px 14px', color: '#334155' }}>Portfolio Showcase & Learning Story</td>
                <td style={{ padding: '12px 14px', color: '#64748b' }}>How to present and explain an Agentic AI architecture professionally for technical reviews</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Agentic AI Architecture Flow */}
      <section className="panel">
        <span className="eyebrow" style={{ color: '#2563eb' }}>Architecture Flow</span>
        <h2 style={{ fontSize: '1.3rem', margin: '6px 0 16px 0' }}>Agentic AI Workflow Pipeline</h2>
        <div style={{ background: '#f8fafc', padding: '20px', borderRadius: '10px', border: '1px solid #e2e8f0', fontFamily: 'monospace', fontSize: '0.85rem', color: '#334155', lineHeight: '1.8' }}>
          Domain Input<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          Shared Workflow Context (`SharedWorkflowContext`)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          LangGraph Conditional Routing (`router_node`) → [Dormant / High-Risk / Standard]<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          Deterministic Agent Nodes (`AttendanceAgent`, `EngagementRiskAgent`, `TrainerAllocationAgent`)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          LLM-Backed Summary Node (`ExplanationSummaryService`)<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          Pydantic Schema Validation & Protected Field Verification<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓ (If Invalid or Error)<br />
          Automatic Deterministic Fallback Trigger<br />
          &nbsp;&nbsp;&nbsp;&nbsp;↓<br />
          Audit Log & Audit Reference Token Generation (`DecisionRecord`)
        </div>
      </section>

      {/* Highlights Grid: LangGraph & LLM */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
        <section className="panel" style={{ margin: 0 }}>
          <span className="eyebrow" style={{ color: '#16a34a' }}>LangGraph Highlights</span>
          <h3 style={{ fontSize: '1.1rem', margin: '6px 0 10px 0' }}>StateGraph & Dynamic Routing</h3>
          <ul style={{ paddingLeft: '18px', margin: 0, fontSize: '0.875rem', color: '#334155', lineHeight: '1.6' }}>
            <li>Replaced static lists with LangGraph `StateGraph`.</li>
            <li>`router_node` evaluates attendance dormancy and churn risk.</li>
            <li>Dynamically skips unnecessary agent nodes for dormant members.</li>
            <li>Records `executed_path` and `skipped_agents` in graph state.</li>
          </ul>
        </section>

        <section className="panel" style={{ margin: 0 }}>
          <span className="eyebrow" style={{ color: '#2563eb' }}>LLM Integration Highlights</span>
          <h3 style={{ fontSize: '1.1rem', margin: '6px 0 10px 0' }}>Validation & Fallback Guardrails</h3>
          <ul style={{ paddingLeft: '18px', margin: 0, fontSize: '0.875rem', color: '#334155', lineHeight: '1.6' }}>
            <li>LLM placed inside `ExplanationSummaryService` node.</li>
            <li>Safe context builder filters prompt context (~300 tokens).</li>
            <li>Pydantic validates JSON schema (`LLMSummaryOutput`).</li>
            <li>Reverts automatically to deterministic rules if LLM fails.</li>
          </ul>
        </section>
      </div>

      {/* 3-5 Minute Student Demo Script */}
      <section className="panel">
        <span className="eyebrow" style={{ color: '#0284c7' }}>Interview Guide</span>
        <h2 style={{ fontSize: '1.3rem', margin: '6px 0 12px 0' }}>3–5 Minute Student Demo Script</h2>
        <div style={{ background: '#f0f9ff', padding: '18px', borderRadius: '10px', border: '1px solid #bae6fd', fontSize: '0.9rem', color: '#0369a1', lineHeight: '1.7' }}>
          <ol style={{ margin: 0, paddingLeft: '20px' }}>
            <li><strong>Introduction:</strong> "Welcome! I am Muhammed Shameel, an Agentic AI Intern at Infocreon. I built the Gym Fitness Member Engagement & Intervention Platform (GFIP)."</li>
            <li><strong>Core Purpose:</strong> "GFIP is a workflow decision-support tool, not an open-ended chatbot. It helps gym staff automatically evaluate member retention risk and assign trainer outreach."</li>
            <li><strong>Deterministic & LangGraph Architecture:</strong> "I started with deterministic agents operating on a shared context, then evolved the workflow into a LangGraph StateGraph with conditional routing that skips redundant steps for inactive members."</li>
            <li><strong>Controlled LLM Integration:</strong> "In Stage 4, I integrated an LLM inside the explanation node to draft qualitative summaries. It is governed by Pydantic schema validation and protected field checks. If the LLM fails or produces malformed JSON, the system automatically falls back to deterministic logic."</li>
            <li><strong>Console & Transparency:</strong> "The Agent Workflow Console allows us to toggle between Deterministic, LangGraph, and LLM-assisted modes side-by-side with complete audit trail visibility."</li>
          </ol>
        </div>
      </section>

      {/* Known Limitations */}
      <section className="panel">
        <span className="eyebrow" style={{ color: '#dc2626' }}>Safety & Boundaries</span>
        <h2 style={{ fontSize: '1.3rem', margin: '6px 0 12px 0' }}>Known Limitations</h2>
        <ul style={{ paddingLeft: '18px', margin: 0, fontSize: '0.875rem', color: '#475569', lineHeight: '1.7' }}>
          <li>This application is an internship MVP built for learning, demonstration, and portfolio presentation.</li>
          <li>It is not a production-grade autonomous AI system and does not perform unreviewed database mutations.</li>
          <li>LLM output is restricted strictly to narrative explanation drafting; core decision rules and risk categories remain protected.</li>
          <li>Recommendations are non-medical and focus strictly on workout habits and facility engagement.</li>
        </ul>
      </section>

      {/* Developer Signature & Footer */}
      <footer className="panel" style={{ background: '#0f172a', color: '#ffffff', border: 'none', padding: '28px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
          <div>
            <h3 style={{ margin: '0 0 6px 0', fontSize: '1.1rem', color: '#ffffff' }}>Infocreon Internship Showcase</h3>
            <p style={{ margin: 0, fontSize: '0.85rem', color: '#94a3b8' }}>
              Built and presented by <strong>Muhammed Shameel</strong> — Agentic AI Intern
            </p>
          </div>
          <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.6', textAlign: 'right' }}>
            <div><strong>Program:</strong> Infocreon Internship</div>
            <div><strong>Project:</strong> GFIP Agentic AI MVP</div>
            <div><strong>Stage Completed:</strong> Stage 1 through Stage 5</div>
            <div><strong>Repository:</strong> <a href="https://github.com/Muhammed-Shameel/GFIP" target="_blank" rel="noreferrer" style={{ color: '#38bdf8', textDecoration: 'underline' }}>github.com/Muhammed-Shameel/GFIP</a></div>
          </div>
        </div>
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', textAlign: 'center', fontSize: '0.8rem', color: '#64748b' }}>
          © 2026 Infocreon Internship. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
