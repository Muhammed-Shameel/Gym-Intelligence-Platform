import { useEffect, useState } from "react";
import { api } from "../api/client";

type WorkflowMode = "deterministic" | "langgraph" | "llm_assisted";

function parseRecommendationItems(recommendation?: string | null) {
  if (!recommendation) return [];
  return recommendation
    .split("|")
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseNarrativeParagraphs(text?: string | null) {
  if (!text) return [];
  return text
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?])\s+(?=[A-Z(])/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function RouteInfo({ data }: { data: any }) {
  if (!data || (data.graph_mode !== "langgraph_stateless" && data.graph_mode !== "langgraph_llm_assisted")) return null;

  return (
    <section className="panel" style={{ background: '#f8f9fa', border: '1px solid #dee2e6' }}>
      <h2>Conditional Routing</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div><strong>Selected Route:</strong> <span className="status-badge">{data.selected_route}</span></div>
        <div><strong>Route Reason:</strong> {data.route_reason}</div>
        <div>
            <strong>Executed Path:</strong> {data.executed_path ? data.executed_path.join(' -> ') : "N/A"}
        </div>
        {data.skipped_agents && data.skipped_agents.length > 0 && (
          <div>
            <strong>Skipped Agents:</strong>
            <ul>
              {data.skipped_agents.map((sa: any, i: number) => (
                <li key={i}>{sa.agent}: {sa.reason}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}

function LLMTracePanel({ data }: { data: any }) {
  if (!data || data.graph_mode !== "langgraph_llm_assisted") return null;

  const modeBadgeColor = data.fallback_used
    ? '#eab308'
    : (data.llm_mode === 'disabled' ? '#64748b' : '#16a34a');

  return (
    <section className="panel" style={{ background: '#f0f9ff', border: '1px solid #bae6fd', marginTop: '15px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h2 style={{ margin: 0, color: '#0369a1', fontSize: '1.2rem' }}>LLM Agent Integration & Audit Trace</h2>
        <span className="status-badge" style={{ background: modeBadgeColor, color: '#fff', padding: '4px 10px', borderRadius: '12px' }}>
          Mode: {data.llm_mode || 'mock'}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', fontSize: '0.875rem' }}>
        <div><strong>Provider:</strong> {data.llm_provider || 'mock'}</div>
        <div><strong>Model:</strong> {data.llm_model || 'mock-agentic-v1'}</div>
        <div><strong>Validation Status:</strong> <span style={{ color: data.llm_validation_status === 'passed' ? '#16a34a' : '#dc2626', fontWeight: 'bold' }}>{data.llm_validation_status || 'passed'}</span></div>

        <div><strong>Fallback Used:</strong> {data.fallback_used ? 'Yes' : 'No'}</div>
        <div style={{ gridColumn: 'span 2' }}><strong>Fallback Reason:</strong> {data.fallback_reason || 'None (LLM validation passed)'}</div>

        <div><strong>Protected Fields Changed:</strong> <span style={{ color: '#16a34a', fontWeight: 'bold' }}>{String(data.protected_fields_changed || false)}</span></div>
        <div style={{ gridColumn: 'span 2' }}><strong>Selected LLM Node:</strong> ExplanationSummaryService (Summary Node)</div>
      </div>
    </section>
  );
}

export function AgentWorkflowConsolePage({ memberId }: { memberId: string }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showDebug, setShowDebug] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [mode, setMode] = useState<WorkflowMode>("llm_assisted");

  const fetchWorkflow = async () => {
    setLoading(true);
    setError("");
    try {
      let response: any;
      if (mode === "deterministic") {
        response = await api.reviewMember(memberId);
      } else if (mode === "langgraph") {
        response = await api.reviewMemberGraph(memberId);
      } else {
        response = await api.reviewMemberLLM(memberId);
      }
      setData(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkflow();
  }, [memberId, mode]);

  const promptAdmin = () => {
    const user = prompt("Enter admin username:");
    const pass = prompt("Enter admin password:");
    if (user === 'admin' && pass === 'admin') {
      setIsAdmin(true);
      setShowDebug(true);
    } else {
      alert("Invalid credentials.");
    }
  };

  if (loading) return <div className="panel"><p>Running {mode.replace('_', ' ')} workflow…</p></div>;
  if (error) return <div className="panel"><p className="error">Error: {error}</p></div>;

  const renderValue = (val: any) => (val === null || val === undefined || (typeof val === 'object' && Object.keys(val).length === 0) ? "N/A" : <pre style={{fontSize: '0.75rem', background: '#f8fafc', padding: '8px', borderRadius: '4px', overflowX: 'auto'}}>{JSON.stringify(val, null, 2)}</pre>);
  
  const isGraphMode = mode === "langgraph" || mode === "llm_assisted";
  const traceLog = (isGraphMode ? data.agent_outputs : data.trace_log) || [];
  const context = (isGraphMode ? data.shared_context : data.context) || {};
  const validationPassed = data.llm_validation_status === "passed" && !data.fallback_used && !data.protected_fields_changed;
  const confidenceLabel = mode === "llm_assisted"
    ? (validationPassed ? "High Confidence" : "Needs Review")
    : "Rule-Based Decision";
  const confidenceClassName = validationPassed || mode !== "llm_assisted"
    ? "confidence-badge"
    : "confidence-badge review";
  const recommendationItems = parseRecommendationItems(data.final_recommendation);
  const explanationParagraphs = parseNarrativeParagraphs(data.explanation || context.explanation);

  return (
    <div className="workflow-console">
      <div className="workflow-header">
        <section className="hero-card" style={{margin: 0, flex: 1}}>
          <h1 style={{ fontSize: '1.5rem', margin: '0 0 4px 0' }}>
            Workflow Console
          </h1>
          <p className="session-id-chip"><span className="chip-label">Section ID:</span> <span>{data.workflow_session_id || data.workflow_id || "N/A"}</span></p>
        </section>
        <div style={{display: 'flex', gap: '12px', alignItems: 'center'}}>
          <button className="status-badge" style={{cursor: 'pointer', border: 'none', padding: '8px 16px', background: isAdmin ? '#16a34a' : '#e2e8f0', color: isAdmin ? '#fff' : '#334155'}} onClick={isAdmin ? () => setShowDebug(!showDebug) : promptAdmin}>
            {isAdmin ? (showDebug ? 'Hide Admin View' : 'Show Admin View') : 'Admin Login'}
          </button>
        </div>
      </div>

      <RouteInfo data={data} />
      
      <section className="panel" style={{ marginTop: '15px' }}>
          <h2>Member Engagement Overview</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div>
              <strong>Trainer Assignment:</strong>
              <p>{data.shared_context?.trainer_assignment?.trainer_id ? `Assigned to: ${data.shared_context.trainer_assignment.trainer_id}` : "No active trainer assigned"}</p>
            </div>
            <div>
              <strong>Follow-up Status:</strong>
              <p>{(data.shared_context?.follow_up_summary?.activities?.length || 0) > 0 ? `${data.shared_context.follow_up_summary.activities.length} recent activities` : "No recent follow-up activities"}</p>
            </div>
          </div>
      </section>

      {isAdmin && <LLMTracePanel data={data} />}

      {isAdmin && (
        <section className="panel" style={{ marginTop: '15px' }}>
          <h2>Agent Sequence Timeline</h2>
          <div className="timeline-wrapper">
            {traceLog.map((log: any, i: number) => (
              <div key={i} className="step-item">
                <div className="step-badge">{i + 1}</div>
                <h3 style={{ fontSize: '1rem', margin: '0 0 6px 0' }}>
                  {log.agent}{' '}
                  {log.agent === 'ExplanationSummaryService' && mode === 'llm_assisted' && (
                    <span className="status-badge" style={{ background: '#2563eb', color: '#fff', marginLeft: '6px' }}>LLM Node</span>
                  )}
                  <span className="status-badge" style={{ marginLeft: '6px' }}>Completed</span>
                </h3>
                {log.started_at && <p style={{fontSize: '0.8rem', color: '#64748b', marginBottom: '10px'}}>Duration: {new Date(log.completed_at).getTime() - new Date(log.started_at).getTime()}ms</p>}
                
                {showDebug && (
                    <div className="data-card">
                      <div style={{display: 'flex', gap: '20px'}}>
                          <div style={{flex: 1}}><strong>Agent Output</strong>{renderValue(log.output)}</div>
                      </div>
                    </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {isAdmin && showDebug && (
        <section className="panel">
          <h2>Shared Workflow Context</h2>
          <div className="context-grid">
              {Object.entries(context).map(([key, value]) => (
                  <div key={key} className="context-section">
                      <h3 style={{fontSize: '0.85rem', marginBottom: '5px', textTransform: 'capitalize', color: '#334155'}}>{key.replace('_', ' ')}</h3>
                      {renderValue(value)}
                  </div>
              ))}
          </div>
        </section>
      )}

      <section className="insight-card">
        <div className="insight-header">
          <div>
            <span className={confidenceClassName}>{confidenceLabel}</span>
            <h2>Final Decision Support</h2>
          </div>
          <span className="output-source-badge">Decision Summary</span>
        </div>

        <div className="decision-block">
          <span className="decision-label">Recommended actions</span>
          {recommendationItems.length > 0 ? (
            <ul className="recommendation-list">
              {recommendationItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="empty-copy">No recommendation returned.</p>
          )}
        </div>

        <div className="explanation-block">
          <span className="decision-label">Explanation</span>
          {explanationParagraphs.length > 0 ? (
            explanationParagraphs.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))
          ) : (
            <p className="empty-copy">No explanation provided.</p>
          )}
        </div>

        <div className="audit-row">
          <span>Audit Reference</span>
          <code>{data.audit_reference || "N/A"}</code>
        </div>
      </section>
    </div>
  );
}
