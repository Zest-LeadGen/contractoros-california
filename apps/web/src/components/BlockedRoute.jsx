export default function BlockedRoute({ title, reason }) {
  return (
    <section className="panel blocked-panel">
      <p className="eyebrow">Blocked route</p>
      <h2>{title}</h2>
      <p>{reason}</p>
      <p className="warning-text">This Phase 3A build has no public, readiness, pass/fail, backend, database, or Question Bank route.</p>
    </section>
  );
}
