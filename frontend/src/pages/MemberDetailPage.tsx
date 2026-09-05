import { useEffect, useState } from "react";
import { api } from "../api/client";

export function MemberDetailPage({ memberId, onBack, onStartWorkflow }: { memberId: string; onBack: () => void; onStartWorkflow: () => void }) {
  const [member, setMember] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.memberById(memberId)
      .then(setMember)
      .catch((err) => setError(err.message));
  }, [memberId]);

  if (error) return <p className="error">Error: {error}</p>;
  if (!member) return <p>Loading member profile…</p>;

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <button className="primary" onClick={onBack}>Back</button>
      </div>

      <section className="panel">
        <div className="detail-header">
          <div>
            <h2 style={{ margin: '0 0 8px 0', fontSize: '2rem' }}>{member.full_name}</h2>
            <div className="identity-row">
                <span className="id-chip"><span className="chip-label">Section ID:</span> <span>{member.member_code}</span></span>
                <span className={`status-badge ${member.status === 'active' ? 'active' : ''}`}>{member.status}</span>
            </div>
          </div>
          <button className="primary" onClick={onStartWorkflow} style={{ padding: '0.75rem 1.5rem' }}>Run Agentic Workflow</button>
        </div>

        <div className="detail-grid">
            <div className="kpi-card" style={{ padding: '1.5rem' }}>
                <span>Email</span>
                <strong style={{ fontSize: '1.1rem' }}>{member.email || "N/A"}</strong>
            </div>
            <div className="kpi-card" style={{ padding: '1.5rem' }}>
                <span>Joined Date</span>
                <strong style={{ fontSize: '1.1rem' }}>{member.joined_on ? new Date(member.joined_on).toLocaleDateString() : "N/A"}</strong>
            </div>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h4>Preferred Training Tags</h4>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {(member.preferred_training_tags || []).map((tag: string, i: number) => (
              <span key={i} className="status-badge">{tag}</span>
            ))}
            {(!member.preferred_training_tags || member.preferred_training_tags.length === 0) && (
              <span style={{ color: 'var(--text-muted)' }}>No tags specified</span>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
