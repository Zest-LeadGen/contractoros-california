import { useMemo, useState } from 'react';
import { claimEligibilityMatrix } from '../data/claimEligibilityMatrix.js';
import ClaimDetailPanel from './ClaimDetailPanel.jsx';

function countBy(items, field) {
  return items.reduce((acc, item) => {
    const value = item[field] || 'Not provided';
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

export default function ClaimGovernanceDashboard() {
  const [selectedId, setSelectedId] = useState(claimEligibilityMatrix[0]?.claim_id || '');
  const [statusFilter, setStatusFilter] = useState('All statuses');
  const statusCounts = useMemo(() => countBy(claimEligibilityMatrix, 'phase_2e_status'), []);
  const riskCounts = useMemo(() => countBy(claimEligibilityMatrix, 'risk_rating'), []);
  const statuses = ['All statuses', ...Object.keys(statusCounts)];
  const filtered = statusFilter === 'All statuses' ? claimEligibilityMatrix : claimEligibilityMatrix.filter((claim) => claim.phase_2e_status === statusFilter);
  const selectedClaim = claimEligibilityMatrix.find((claim) => claim.claim_id === selectedId) || claimEligibilityMatrix[0];
  const draftingCandidates = claimEligibilityMatrix.filter((claim) => claim.phase_2e_status === 'Drafting Candidate Later').length;
  const legalReview = claimEligibilityMatrix.filter((claim) => claim.phase_2e_status === 'Legal Review Required Before Drafting').length;
  const retired = claimEligibilityMatrix.filter((claim) => claim.phase_2e_status === 'Retired from pilot').length;
  const narrowed = claimEligibilityMatrix.filter((claim) => claim.phase_2e_status === 'Narrowed/Split Claim Created').length;

  return (
    <section className="panel governance-panel">
      <div className="section-heading">
        <p className="eyebrow">Internal claim governance fixture</p>
        <h2>Phase 2E claim eligibility matrix</h2>
        <p className="muted">These are internal source claims. They are not MCQs and not Question Bank records.</p>
      </div>
      <div className="metric-grid">
        <div className="metric"><span>Total claims</span><strong>{claimEligibilityMatrix.length}</strong></div>
        <div className="metric"><span>Drafting candidates later</span><strong>{draftingCandidates}</strong></div>
        <div className="metric"><span>Legal review required</span><strong>{legalReview}</strong></div>
        <div className="metric"><span>Retired claims</span><strong>{retired}</strong></div>
        <div className="metric"><span>Narrowed child claims</span><strong>{narrowed}</strong></div>
      </div>
      <div className="counts-grid">
        <div><h3>Count by Phase 2E status</h3><ul>{Object.entries(statusCounts).map(([key, value]) => <li key={key}>{key}: <strong>{value}</strong></li>)}</ul></div>
        <div><h3>Count by risk rating</h3><ul>{Object.entries(riskCounts).map(([key, value]) => <li key={key}>{key}: <strong>{value}</strong></li>)}</ul></div>
      </div>
      <label className="filter-label">Filter by status
        <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>{statuses.map((status) => <option key={status} value={status}>{status}</option>)}</select>
      </label>
      <div className="governance-layout">
        <div className="claim-table-wrap">
          <table className="claim-table"><thead><tr><th>Claim ID</th><th>Risk</th><th>Status</th><th>MCQ status</th></tr></thead><tbody>{filtered.map((claim) => <tr key={claim.claim_id} className={selectedId === claim.claim_id ? 'selected-row' : ''} onClick={() => setSelectedId(claim.claim_id)}><td>{claim.claim_id}</td><td>{claim.risk_rating || 'Not provided'}</td><td>{claim.phase_2e_status || 'Not provided'}</td><td>{claim.mcq_status || 'Not provided'}</td></tr>)}</tbody></table>
        </div>
        <ClaimDetailPanel claim={selectedClaim} />
      </div>
    </section>
  );
}
