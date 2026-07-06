export default function DomainBrowser({ domains, selectedDomain, setSelectedDomain }) {
  return (
    <section className="panel compact-panel">
      <label className="filter-label">
        Law & Business domain
        <select value={selectedDomain} onChange={(event) => setSelectedDomain(event.target.value)}>
          {domains.map((domain) => <option key={domain} value={domain}>{domain}</option>)}
        </select>
      </label>
      <p className="muted">Static local fixture data only. Domain browsing does not imply public release or readiness.</p>
    </section>
  );
}
