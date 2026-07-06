const fields = [
  ['claim_id', 'Claim ID'],
  ['parent_claim_id', 'Parent claim ID'],
  ['source_url', 'Source URL'],
  ['statute_section_anchor', 'Source anchor'],
  ['risk_rating', 'Risk rating'],
  ['phase_2e_status', 'Phase 2E status'],
  ['exception_limitation_note', 'Exception / limitation note'],
  ['source_access_date', 'Source access date'],
  ['legal_currentness_verified_date', 'Legal/currentness verified date'],
  ['currentness_status', 'Currentness status'],
  ['promotion_recommendation', 'Promotion recommendation'],
  ['mcq_status', 'MCQ status'],
  ['public_use_status', 'Public use status'],
  ['contamination_status', 'Contamination status'],
  ['reviewer_notes', 'Reviewer notes']
];

function valueOrFallback(value) {
  return value && String(value).trim() ? value : 'Not provided';
}

export default function ClaimDetailPanel({ claim }) {
  if (!claim) return <aside className="claim-detail"><h3>No claim selected</h3></aside>;
  return (
    <aside className="claim-detail">
      <h3>Claim detail</h3>
      <p className="muted">Source claim only. Not an MCQ, not public content, not a Question Bank record, and not publication eligible.</p>
      <dl className="metadata-grid compact-grid">
        {fields.map(([key, label]) => (
          <div key={key}>
            <dt>{label}</dt>
            <dd>{key === 'source_url' && claim[key] ? <a href={claim[key]} target="_blank" rel="noreferrer">{claim[key]}</a> : valueOrFallback(claim[key])}</dd>
          </div>
        ))}
      </dl>
    </aside>
  );
}
