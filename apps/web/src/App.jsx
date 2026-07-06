import { useMemo, useState } from 'react';
import Layout from './components/Layout.jsx';
import TrackSelect from './components/TrackSelect.jsx';
import DomainBrowser from './components/DomainBrowser.jsx';
import QuestionPlayer from './components/QuestionPlayer.jsx';
import BlockedRoute from './components/BlockedRoute.jsx';
import AdminPlaceholder from './components/AdminPlaceholder.jsx';
import ClaimGovernanceDashboard from './components/ClaimGovernanceDashboard.jsx';
import { internalFixtureItems } from './data/internalFixtureItems.js';

const blockedRoutes = {
  readiness: { title: 'Readiness scoring blocked', reason: 'Readiness scoring is not approved in Phase 3A.' },
  passFail: { title: 'Pass/fail logic blocked', reason: 'Pass/fail predictions are not approved in Phase 3A.' },
  publicLaunch: { title: 'Public launch blocked', reason: 'Public launch requires future legal, content, and build-readiness gates.' },
  c10Public: { title: 'C10 public content blocked', reason: 'C10 deferred until currentness/safety gate approval.' },
  backend: { title: 'Backend/database blocked', reason: 'No backend or database is connected in Phase 3A.' },
  questionBank: { title: 'Question Bank migration blocked', reason: 'No content is approved for Question Bank migration in Phase 3A.' }
};

export default function App() {
  const [view, setView] = useState('practice');
  const [selectedTrack, setSelectedTrack] = useState('Law & Business');
  const [selectedDomain, setSelectedDomain] = useState('All domains');
  const [blockedKey, setBlockedKey] = useState('readiness');

  const domains = useMemo(() => ['All domains', ...Array.from(new Set(internalFixtureItems.map((item) => item.domain)))], []);
  const filteredItems = useMemo(() => selectedDomain === 'All domains' ? internalFixtureItems : internalFixtureItems.filter((item) => item.domain === selectedDomain), [selectedDomain]);
  const openBlocked = (key) => { setBlockedKey(key); setView('blocked'); };

  return (
    <Layout view={view} setView={setView} openBlocked={openBlocked}>
      {view === 'practice' && (
        <div className="stack">
          <TrackSelect selectedTrack={selectedTrack} setSelectedTrack={setSelectedTrack} openBlocked={openBlocked} />
          <DomainBrowser domains={domains} selectedDomain={selectedDomain} setSelectedDomain={setSelectedDomain} />
          <QuestionPlayer items={filteredItems} />
        </div>
      )}
      {view === 'governance' && <ClaimGovernanceDashboard />}
      {view === 'admin' && <AdminPlaceholder />}
      {view === 'blocked' && <BlockedRoute {...blockedRoutes[blockedKey]} />}
    </Layout>
  );
}
