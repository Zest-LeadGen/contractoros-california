export const trackStatuses = [
  {
    id: 'law-business',
    title: 'Law & Business',
    status: 'Active internal fixture track',
    description: 'Visible only as internal fixture content for scaffold testing.'
  },
  {
    id: 'c10-electrical',
    title: 'C10 Electrical',
    status: 'Deferred / blocked',
    description: 'C10 remains blocked until a separate approval gate.'
  }
];

export const internalQuestion = {
  id: 'law-business-internal-placeholder-001',
  track: 'Law & Business',
  label: 'Internal fixture placeholder only',
  prompt: 'Internal scaffold check: what is this mobile shell?',
  choices: [
    { id: 'a', text: 'Approved release build.' },
    { id: 'b', text: 'Internal fixture-only prototype.' },
    { id: 'c', text: 'Outcome engine.' },
    { id: 'd', text: 'Remote account workflow.' }
  ],
  correctChoiceId: 'b',
  feedback: 'Internal QA feedback only: this scaffold is local fixture content.'
};
