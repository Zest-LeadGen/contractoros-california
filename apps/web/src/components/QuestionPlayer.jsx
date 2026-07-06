import { useEffect, useState } from 'react';
import SourcePanel from './SourcePanel.jsx';
import IssueReportPanel from './IssueReportPanel.jsx';

export default function QuestionPlayer({ items }) {
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState('');
  const [submitted, setSubmitted] = useState({});
  const [showSource, setShowSource] = useState(false);
  const [showIssue, setShowIssue] = useState(false);

  useEffect(() => {
    setIndex(0);
    setSelected('');
    setShowSource(false);
    setShowIssue(false);
  }, [items]);

  const item = items[index];
  if (!item) return <section className="panel"><h2>No fixture items available</h2></section>;

  const submittedAnswer = submitted[item.itemId] || '';
  const isSubmitted = Boolean(submittedAnswer);

  const submitAnswer = () => {
    if (!selected || isSubmitted) return;
    setSubmitted((current) => ({ ...current, [item.itemId]: selected }));
  };

  const move = (delta) => {
    const next = index + delta;
    if (next < 0 || next >= items.length) return;
    setIndex(next);
    setSelected('');
    setShowSource(false);
    setShowIssue(false);
  };

  return (
    <section className="panel question-panel">
      <div className="question-header">
        <div>
          <p className="eyebrow">Internal fixture practice item</p>
          <h2>{item.itemId}</h2>
          <p className="muted">{item.track} / {item.domain}</p>
        </div>
        <span className="status-pill">{Object.keys(submitted).length} of {items.length} fixture items submitted</span>
      </div>

      <p className="warning-text">Internal fixture only. No score, readiness, pass/fail, or recommendation exists.</p>
      <h3>{item.question}</h3>

      <div className="choices">
        {item.choices.map((choice) => {
          const active = (isSubmitted ? submittedAnswer : selected) === choice.letter;
          const correct = isSubmitted && item.correctAnswer === choice.letter;
          return (
            <button key={choice.letter} disabled={isSubmitted} className={active ? 'choice selected' : 'choice'} onClick={() => setSelected(choice.letter)}>
              <strong>{choice.letter}.</strong> {choice.text} {correct ? <span className="correct-label">Correct</span> : null}
            </button>
          );
        })}
      </div>

      {!isSubmitted && <button disabled={!selected} onClick={submitAnswer}>Submit answer</button>}
      {isSubmitted && <div className="feedback-box"><p><strong>Selected answer:</strong> {submittedAnswer}</p><p><strong>Correct answer:</strong> {item.correctAnswer}</p><p><strong>Explanation:</strong> {item.explanation}</p></div>}

      <div className="button-row">
        <button disabled={index === 0} onClick={() => move(-1)}>Back</button>
        <button disabled={index === items.length - 1} onClick={() => move(1)}>Next</button>
        <button onClick={() => setShowSource((value) => !value)}>Source / claim</button>
        <button onClick={() => setShowIssue((value) => !value)}>Report issue</button>
      </div>
      {showSource && <SourcePanel item={item} />}
      {showIssue && <IssueReportPanel item={item} submittedAnswer={submittedAnswer || selected || 'None'} />}
    </section>
  );
}
