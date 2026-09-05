import { useState } from "react";
import type { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
  activeSection: 'dashboard' | 'members' | 'other';
  onNavigate: (section: 'dashboard' | 'members' | 'admin') => void;
}

export function Layout({ children, activeSection, onNavigate }: LayoutProps) {
  const [showDevDetails, setShowDevDetails] = useState(false);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <h1 style={{ cursor: 'pointer', fontSize: '1.25rem' }} onClick={() => onNavigate('dashboard')}>Gym Intelligence</h1>
        </div>

        <nav style={{ marginTop: '20px' }}>
          <a href="#" className={activeSection === 'dashboard' ? 'nav-item active' : 'nav-item'} onClick={(e) => { e.preventDefault(); onNavigate('dashboard'); }}>Dashboard</a>
          <a href="#" className={activeSection === 'members' ? 'nav-item active' : 'nav-item'} onClick={(e) => { e.preventDefault(); onNavigate('members'); }}>All Members</a>
        </nav>

        <div style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
             <button onClick={() => { onNavigate('admin'); }} style={{ background: 'transparent', border: '1px solid #475569', color: '#cbd5e1', padding: '4px 12px', borderRadius: '4px', fontSize: '0.75rem', cursor: 'pointer' }}>Admin</button>
             <button 
                onClick={() => setShowDevDetails(true)} 
                style={{ background: 'transparent', border: '1px solid #475569', color: '#cbd5e1', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                title="Developer Details"
             >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
             </button>
        </div>
      </aside>

      <main>{children}</main>

      {showDevDetails && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }} onClick={() => setShowDevDetails(false)}>
          <div className="panel" style={{ width: '340px', textAlign: 'center' }} onClick={e => e.stopPropagation()}>
            <h3 style={{ margin: '0 0 0.5rem 0' }}>Muhammed Shameel</h3>
            <p style={{ color: 'var(--primary)', fontSize: '0.9rem', fontWeight: 600, margin: '0 0 1.5rem 0' }}>AI Engineer | Data Scientist</p>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', marginTop: '1rem' }}>
              <a href="https://www.linkedin.com/in/muhammed-shameel" target="_blank" rel="noopener noreferrer" style={{ display: 'flex', alignItems: 'center', color: 'var(--primary)', textDecoration: 'none', fontWeight: 600, padding: '0.5rem 1rem', border: '1px solid var(--primary)', borderRadius: '0.5rem' }}>
                 <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style={{ marginRight: '8px' }}><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                 LinkedIn Profile
              </a>
            </div>
            <p style={{ marginTop: '2rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>Internal Version v1.0</p>
            <div style={{ marginTop: '10px' }}>
              <button onClick={() => setShowDevDetails(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
