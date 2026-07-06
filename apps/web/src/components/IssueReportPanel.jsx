import { useState } from 'react';

export default function IssueReportPanel({ item, submittedAnswer }) {
  const [category, setCategory] = useState('');
  const [note, setNote] = useState('');
  const [mockSaved, setMockSaved] = useState(false);

  const submitMockIssue = () => {
    if (!category) return;
    setMockSaved(true);
  };

  return (
    <aside className="issue-panel">
      <h3>Issue report mock</h3>
      <p className="warning-text">Mock issue only. Nothing is saved, synced, or submitted.</p>
      <dl className="metadata-grid compact-grid">
        <div><dt>Item ID</dt><dd>{item.itemId}</dd></div>
        <div><dt>Selected answer snapshot</dt><dd>{submittedAnswer || 'None'}</dd></div>
      </dl>
      <label className="filter-label">Issue category
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="">Select category</option>
          <option>Wording unclear</option>
          <option>Source concern</option>
          <option>Possible legal-risk wording</option>
          <option>Fixture/UI bug</option>
        </select>
      </label>
      <label className="filter-label">Reviewer note
        <textarea value={note} onChange={(event) => setNote(event.target.value)} placeholder="Internal reviewer note only" />
      </label>
      <button disabled={!category} onClick={submitMockIssue}>Submit mock issue</button>
      {mockSaved && <p className="success-text">Mock issue stored in temporary in-memory state only. Nothing was saved or synced.</p>}
    </aside>
  );
}
