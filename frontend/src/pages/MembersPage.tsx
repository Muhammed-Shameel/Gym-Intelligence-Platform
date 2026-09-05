import { useState, useEffect } from "react";
import { api } from "../api/client";
import type { Member } from "../types";

export function MembersPage({ onMemberSelect }: { onMemberSelect: (id: string) => void }) {
  const [members, setMembers] = useState<Member[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.members()
      .then((data) => setMembers(data.items))
      .finally(() => setLoading(false));
  }, []);

  const filteredMembers = members.filter(m => 
    m.full_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    m.member_code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>All Members ({members.length})</h2>
        <input 
          type="text" 
          placeholder="Search by name or code..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border)' }}
        />
      </div>
      
      {loading ? <p>Loading...</p> : (
        <div className="member-grid">
          {filteredMembers.map((member) => (
            <article key={member.id} className="member-card" onClick={() => onMemberSelect(member.id)} style={{ cursor: 'pointer' }}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem'}}>
                <span className="eyebrow" style={{fontFamily: 'monospace'}}>{member.member_code}</span>
                <span className={`status-badge ${member.status === 'active' ? 'active' : ''}`}>{member.status}</span>
              </div>
              <h3 style={{margin: 0}}>{member.full_name}</h3>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
