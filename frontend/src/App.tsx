import { useState } from "react";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./pages/DashboardPage";
import { MembersPage } from "./pages/MembersPage";
import { MemberDetailPage } from "./pages/MemberDetailPage";
import { AgentWorkflowConsolePage } from "./pages/AgentWorkflowConsolePage";
import { AdminPage } from "./pages/AdminPage";

export default function App() {
  const [view, setView] = useState<
    { type: 'dashboard' } | 
    { type: 'members' } |
    { type: 'memberDetail', id: string } | 
    { type: 'workflowConsole', id: string } |
    { type: 'admin' }
  >({ type: 'dashboard' });

  const [activeSection, setActiveSection] = useState<'dashboard' | 'members' | 'other'>('dashboard');

  const handleNavigate = (section: 'dashboard' | 'members' | 'admin') => {
    if (section === 'admin') {
      setView({ type: 'admin' });
      setActiveSection('other');
      return;
    }
    if (section === 'members') {
      setView({ type: 'members' });
      setActiveSection('members');
      return;
    }
    setActiveSection('dashboard');
    setView({ type: 'dashboard' });
  };

  const handleMemberSelect = (id: string) => {
    setActiveSection('other');
    setView({ type: 'memberDetail', id });
  }

  return (
    <Layout activeSection={activeSection} onNavigate={handleNavigate}>
      {view.type === 'dashboard' && (
        <DashboardPage 
          onMemberSelect={handleMemberSelect}
          onViewAll={() => handleNavigate('members')}
        />
      )}
      {view.type === 'members' && (
        <MembersPage onMemberSelect={handleMemberSelect} />
      )}
      {view.type === 'memberDetail' && (
        <MemberDetailPage 
          memberId={view.id} 
          onBack={() => {
            setActiveSection('dashboard');
            setView({ type: 'dashboard' });
          }} 
          onStartWorkflow={() => {
            setActiveSection('other');
            setView({ type: 'workflowConsole', id: view.id });
          }} 
        />
      )}
      {view.type === 'workflowConsole' && (
        <AgentWorkflowConsolePage memberId={view.id} />
      )}
      {view.type === 'admin' && (
        <AdminPage onBack={() => handleNavigate('dashboard')} />
      )}
    </Layout>
  );
}
