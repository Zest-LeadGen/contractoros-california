import InternalBanner from './InternalBanner.jsx';

export default function Layout({ children, view, setView, openBlocked }) {
  const navItems = [
    ['practice', 'Practice Flow'],
    ['governance', 'Claim Governance'],
    ['admin', 'Admin Placeholder']
  ];
  return (
    <div className="app-shell">
      <InternalBanner />
      <header className="hero">
        <p className="eyebrow">ContractorOS California</p>
        <h1>Phase One Internal Scaffold</h1>
        <p>Fixture-only Law & Business learner flow plus internal claim-governance view. No backend, scoring, readiness, or public content.</p>
      </header>
      <nav className="nav-card">
        {navItems.map(([key, label]) => (
          <button key={key} className={view === key ? 'active' : ''} onClick={() => setView(key)}>{label}</button>
        ))}
        <button onClick={() => openBlocked('readiness')}>Blocked: Readiness</button>
        <button onClick={() => openBlocked('passFail')}>Blocked: Pass/Fail</button>
        <button onClick={() => openBlocked('publicLaunch')}>Blocked: Public Launch</button>
        <button onClick={() => openBlocked('c10Public')}>Blocked: C10 Public</button>
        <button onClick={() => openBlocked('backend')}>Blocked: Backend</button>
        <button onClick={() => openBlocked('questionBank')}>Blocked: Question Bank</button>
      </nav>
      <main>{children}</main>
    </div>
  );
}
