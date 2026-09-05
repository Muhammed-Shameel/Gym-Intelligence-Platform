import { useState, useEffect } from "react";
import { api } from "../api/client";

export function AdminPage({ onBack }: { onBack: () => void }) {
  const [password, setPassword] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState<'members' | 'trainers'>('members');
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    if (isAuthenticated) {
      if (activeTab === 'members') {
        api.members().then((res) => setData(res.items));
      } else {
        api.trainers().then((res) => setData(res.items));
      }
    }
  }, [isAuthenticated, activeTab]);

  if (!isAuthenticated) {
    return (
      <div className="panel" style={{ maxWidth: '400px', margin: '40px auto' }}>
        <h2>Admin Access</h2>
        <input 
          type="password" 
          placeholder="Enter password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: '100%', padding: '12px', marginBottom: '16px', borderRadius: '6px', border: '1px solid var(--border)' }}
        />
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="primary" style={{ flex: 1 }} onClick={() => { if (password === 'admin') setIsAuthenticated(true); else alert('Wrong password'); }}>Login</button>
          <button style={{ flex: 1 }} onClick={onBack}>Cancel</button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>Admin Hub</h2>
        <button onClick={onBack}>Back to Dashboard</button>
      </div>
      
      <div className="panel" style={{ padding: '16px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => setActiveTab('members')} className={activeTab === 'members' ? 'status-badge tab-active' : 'status-badge'}>Members</button>
          <button onClick={() => setActiveTab('trainers')} className={activeTab === 'trainers' ? 'status-badge tab-active' : 'status-badge'}>Trainers</button>
        </div>
      </div>

      <div className="panel">
        <input type="text" placeholder={`Search ${activeTab}...`} style={{ width: '100%', padding: '12px', marginBottom: '20px', borderRadius: '6px', border: '1px solid var(--border)' }} />
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--border)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '12px 0' }}>Code</th>
              <th style={{ padding: '12px 0' }}>Name</th>
              <th style={{ padding: '12px 0' }}>{activeTab === 'members' ? 'Status' : 'Skills'}</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '16px 0', fontFamily: 'monospace', color: 'var(--primary)' }}>{item.member_code || item.trainer_code}</td>
                <td style={{ padding: '16px 0', fontWeight: 600 }}>{item.full_name}</td>
                <td style={{ padding: '16px 0' }}>{activeTab === 'members' ? <span className={`status-badge ${item.status === 'active' ? 'active' : ''}`}>{item.status}</span> : item.skill_tags?.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
