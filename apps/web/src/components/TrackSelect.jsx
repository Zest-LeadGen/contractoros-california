export default function TrackSelect({ selectedTrack, setSelectedTrack, openBlocked }) {
  return (
    <section className="panel">
      <div className="section-heading">
        <p className="eyebrow">Track selection</p>
        <h2>Select a license track</h2>
      </div>
      <div className="track-grid">
        <button className={selectedTrack === 'Law & Business' ? 'track-card selected' : 'track-card'} onClick={() => setSelectedTrack('Law & Business')}>
          <strong>Law & Business</strong>
          <span>Available as internal development fixture only.</span>
        </button>
        <button className="track-card locked" disabled onClick={() => openBlocked('c10Public')}>
          <strong>C10 Electrical</strong>
          <span>C10 deferred until currentness/safety gate approval.</span>
        </button>
      </div>
    </section>
  );
}
