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
      <div style={{ marginBottom: '15px' }}>
        <button 
          onClick={onBack}
          style={{ background: 'transparent', border: '1px solid #cbd5e1', padding: '6px 14px', borderRadius: '6px', cursor: 'pointer', color: '#475569', fontWeight: '600', fontSize: '0.85rem' }}
        >
          Back to Dashboard
        </button>
      </div>

      <section className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div>
            <span className="eyebrow" style={{ color: '#2563eb' }}>Member Profile</span>
            <h2 style={{ margin: '5px 0 0 0', fontSize: '1.6rem' }}>{member.full_name}</h2>
          </div>
          <span className={`status-badge ${member.status === 'active' ? 'active' : ''}`} style={{ fontSize: '0.85rem', padding: '4px 12px' }}>
            {member.status}
          </span>
        </div>

        <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '20px' }}>
          <article>
            <span>Member Code</span>
            <strong style={{ fontFamily: 'monospace', color: '#1e293b' }}>{member.member_code}</strong>
          </article>
          <article>
            <span>Email</span>
            <strong style={{ fontSize: '1rem', color: '#334155' }}>{member.email || "N/A"}</strong>
          </article>
          <article>
            <span>Joined Date</span>
            <strong style={{ fontSize: '1rem', color: '#334155' }}>{member.joined_on ? new Date(member.joined_on).toLocaleDateString() : "N/A"}</strong>
          </article>
        </div>

        <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '10px', border: '1px solid #e2e8f0', marginBottom: '20px' }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#334155', fontSize: '0.9rem' }}>Preferred Training Tags</h4>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {(member.preferred_training_tags || []).map((tag: string, i: number) => (
              <span key={i} style={{ background: '#e0f2fe', color: '#0369a1', padding: '4px 10px', borderRadius: '12px', fontSize: '0.85rem', fontWeight: '600' }}>
                {tag}
              </span>
            ))}
            {(!member.preferred_training_tags || member.preferred_training_tags.length === 0) && (
              <span style={{ color: '#94a3b8', fontSize: '0.85rem' }}>No tags specified</span>
            )}
          </div>
        </div>

        <div style={{ paddingTop: '15px', borderTop: '1px solid #e2e8f0', display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            onClick={onStartWorkflow} 
            style={{ background: '#2563eb', color: 'white', padding: '10px 24px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: '600', fontSize: '0.9rem' }}
          >
            Run Agentic Workflow Console
          </button>
        </div>
      </section>
    </div>
  );
}
