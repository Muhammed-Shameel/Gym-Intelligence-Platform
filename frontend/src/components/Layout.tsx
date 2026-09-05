import type { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
  activeSection: 'dashboard' | 'members' | 'other';
  onNavigate: (section: 'dashboard' | 'members' | 'admin') => void;
}

export function Layout({ children, activeSection, onNavigate }: LayoutProps) {
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

        <div style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid rgba(255,255,255,0.08)', fontSize: '0.75rem', color: '#64748b' }}>
          Internal Version v1.0 
          <a href="#" style={{ color: '#475569', marginLeft: '5px', textDecoration: 'none' }} onClick={(e) => { e.preventDefault(); onNavigate('admin'); }}>[Admin]</a>
        </div>
      </aside>

      <main>{children}</main>
    </div>
  );
}
