import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Member } from "../types";

type JoinTrendPoint = {
  month: string;
  label: string;
  count: number;
};

function buildIntegerTicks(maxValue: number) {
  const safeMax = Math.max(maxValue, 1);
  const step = safeMax <= 5 ? 1 : Math.ceil(safeMax / 4);
  const ticks: number[] = [];

  for (let tick = 0; tick <= safeMax; tick += step) {
    ticks.push(tick);
  }

  if (ticks[ticks.length - 1] !== safeMax) {
    ticks.push(safeMax);
  }

  return ticks;
}

function MemberJoinTrendChart({ data }: { data: JoinTrendPoint[] }) {
  if (data.length === 0) {
    return <div className="empty-state">No join trend data available.</div>;
  }

  const maxCount = Math.max(...data.map((point) => point.count), 1);
  const ticks = buildIntegerTicks(maxCount);
  const width = 640;
  const height = 228;
  const margin = { top: 24, right: 18, bottom: 40, left: 42 };
  const chartWidth = width - margin.left - margin.right;
  const chartHeight = height - margin.top - margin.bottom;
  const slotWidth = chartWidth / data.length;
  const barWidth = Math.min(34, Math.max(12, slotWidth * 0.48));

  return (
    <div className="chart-frame" aria-label="Member join trend by month">
      <svg className="join-trend-chart" viewBox={`0 0 ${width} ${height}`} role="img">
        <title>Member Join Trends</title>
        <desc>Monthly member joins scaled from zero to {maxCount} members.</desc>
        {ticks.map((tick) => {
          const y = margin.top + chartHeight - (tick / maxCount) * chartHeight;
          return (
            <g key={tick}>
              <line
                className="chart-grid-line"
                x1={margin.left}
                x2={width - margin.right}
                y1={y}
                y2={y}
              />
              <text className="chart-axis-label" x={margin.left - 12} y={y + 4} textAnchor="end">
                {tick}
              </text>
            </g>
          );
        })}

        {data.map((point, index) => {
          const barHeight = (point.count / maxCount) * chartHeight;
          const x = margin.left + index * slotWidth + (slotWidth - barWidth) / 2;
          const y = margin.top + chartHeight - barHeight;

          return (
            <g key={point.month} className="chart-bar-group">
              <rect
                className="chart-bar"
                x={x}
                y={y}
                width={barWidth}
                height={Math.max(barHeight, 2)}
                rx="5"
              >
                <title>{`${point.month}: ${point.count} member${point.count === 1 ? "" : "s"}`}</title>
              </rect>
              <text className="chart-value-label" x={x + barWidth / 2} y={Math.max(y - 8, 12)} textAnchor="middle">
                {point.count}
              </text>
              <text className="chart-month-label" x={x + barWidth / 2} y={height - 14} textAnchor="middle">
                {point.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

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
  const joinTrendData = sortedMonths.map((month) => ({
    month,
    label: month.split('-')[1],
    count: monthlyJoinCounts[month],
  }));

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

      <div className="analytics-grid">
        <section className="panel">
          <h2>Member Join Trends</h2>
          <MemberJoinTrendChart data={joinTrendData} />
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
            <div className="activity-grid">
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
