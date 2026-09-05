import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Member } from "../types";

export function DashboardPage({ onMemberSelect, onViewAll }: { onMemberSelect: (id: string) => void, onViewAll: () => void }) {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.members()
      .then((data) => setMembers(data.items))
      .finally(() => setLoading(false));
  }, []);

  const activeCount = members.filter(m => m.status === 'active').length;
  const tagCounts = members.reduce((acc: Record<string, number>, m) => {
    m.preferred_training_tags.forEach(tag => acc[tag] = (acc[tag] || 0) + 1);
    return acc;
  }, {});
  const monthlyJoinCounts = members.reduce((acc: Record<string, number>, m) => {
    const month = m.joined_on.substring(0, 7);
    acc[month] = (acc[month] || 0) + 1;
    return acc;
  }, {});
  const sortedMonths = Object.keys(monthlyJoinCounts).sort();
  const maxCount = Math.max(...Object.values(monthlyJoinCounts), 1);

  return (
    <>
      <section className="hero-card">
        <p className="eyebrow">Engagement Center</p>
        <h2>Gym Intelligence Platform</h2>
      </section>

      <section className="kpi-grid">
        <article className="kpi-card">
          <span>Total Members</span>
          <strong>{members.length}</strong>
        </article>
        <article className="kpi-card">
          <span>Active Status</span>
          <strong style={{ color: 'var(--primary)' }}>{activeCount}</strong>
        </article>
        <article className="kpi-card">
          <span>Inactive/Paused</span>
          <strong style={{ color: 'var(--text-muted)' }}>{members.length - activeCount}</strong>
        </article>
      </section>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
        <section className="panel">
          <h2>Member Join Trends</h2>
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end', height: '140px', paddingBottom: '20px' }}>
            {sortedMonths.map(month => {
              const height = (monthlyJoinCounts[month] / maxCount) * 100;
              return (
                <div key={month} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '100%', background: 'var(--primary)', height: `${height}%`, minHeight: '8px', borderRadius: '4px' }} title={`${month}: ${monthlyJoinCounts[month]}`}></div>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{month.split('-')[1]}</span>
                </div>
              );
            })}
          </div>
        </section>
        <section className="panel">
          <h2>Popular Training Tags</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {Object.entries(tagCounts).sort((a,b) => b[1] - a[1]).map(([tag, count]) => (
              <div key={tag}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                    <span>{tag}</span>
                    <span style={{ fontWeight: 600 }}>{count}</span>
                </div>
                <div style={{ width: '100%', background: 'var(--border)', height: '8px', borderRadius: '4px' }}>
                    <div style={{ width: `${(count / members.length) * 100}%`, background: 'var(--primary)', height: '8px', borderRadius: '4px' }}></div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>Recent Member Activity</h2>
          <button className="primary" onClick={onViewAll}>View All</button>
        </div>
        {loading ? <p>Loading...</p> : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
            {members.slice(0, 6).map((member) => (
                <div key={member.id} className="kpi-card" onClick={() => onMemberSelect(member.id)} style={{ cursor: 'pointer', padding: '1rem' }}>
                    <span className="eyebrow" style={{fontSize: '0.6rem'}}>{member.member_code}</span>
                    <div style={{ fontWeight: 600, marginTop: '0.25rem' }}>{member.full_name}</div>
                </div>
            ))}
            </div>
        )}
      </section>
    </>
  );
}
