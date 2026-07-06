export default function SourcePanel({ item }) {
  if (!item) return null;
  return (
    <aside className="source-panel">
      <h3>Source / claim metadata</h3>
      <dl className="metadata-grid">
        <div><dt>Source URL</dt><dd><a href={item.sourceUrl} target="_blank" rel="noreferrer">{item.sourceUrl}</a></dd></div>
        <div><dt>Claim ID</dt><dd>{item.claimId}</dd></div>
        <div><dt>Content status</dt><dd>{item.contentStatus}</dd></div>
        <div><dt>Legal review status</dt><dd>{item.legalReviewStatus}</dd></div>
        <div><dt>Public eligibility status</dt><dd>{item.publicEligibilityStatus}</dd></div>
      </dl>
      <p className="warning-text">No legal approval, public approval, CSLB affiliation, PSI affiliation, or Question Bank approval is implied.</p>
    </aside>
  );
}
