const URLs = {
  u7031: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7031',
  u7068: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7068.',
  u7071: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7071.6',
  u7159: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7159.',
  u71595: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=7159.5',
  u8200: 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=8200'
};

const base = {
  track: 'Law & Business',
  source_access_date: '2026-07-05',
  legal_currentness_verified_date: 'NOT VERIFIED — requires legal/currentness review',
  currentness_status: 'Accessed only; not legally/currently verified',
  mcq_status: 'No MCQ created',
  public_use_status: 'Not public; not publication eligible',
  contamination_status: 'Clean — official source only',
  exception_limitation_note: 'Limitations and exceptions must be reviewed before future drafting.',
  promotion_recommendation: 'See Phase 2E status. Future drafting requires later approval.',
  reviewer_notes: 'Internal source-claim fixture only.'
};

function row(claim_id, parent_claim_id, domain_category, source_url, statute_section_anchor, risk_rating, phase_2e_status) {
  return { ...base, claim_id, parent_claim_id, domain_category, source_url, statute_section_anchor, risk_rating, phase_2e_status };
}

export const claimEligibilityMatrix = [
  row('CLM-P2C-LAW-001','', 'Business Organization & Licensing', URLs.u7031, 'BPC §7031(a)', 'High', 'Legal Review Required Before Drafting'),
  row('CLM-P2C-LAW-002','', 'Business Organization & Licensing', URLs.u7031, 'BPC §7031(b)', 'High', 'Legal Review Required Before Drafting'),
  row('CLM-P2C-LAW-003','', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(a)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-004','', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(b)(1)-(4)', 'Medium', 'Retired from pilot'),
  row('CLM-P2E-LAW-004A','CLM-P2C-LAW-004', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(b)(1)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-004B','CLM-P2C-LAW-004', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(b)(2)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-004C','CLM-P2C-LAW-004', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(b)(3)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-004D','CLM-P2C-LAW-004', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(b)(4)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2C-LAW-005','', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(c)(1)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-006','', 'Business Organization & Licensing', URLs.u7068, 'BPC §7068(c)(2)(B)', 'Medium', 'Source/Currentness Recheck Required'),
  row('CLM-P2C-LAW-007','', 'Bonds / Licensing', URLs.u7071, 'BPC §7071.6(a)', 'Low', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-008','', 'Bonds / Licensing', URLs.u7071, 'BPC §7071.6(c)', 'Medium', 'Legal Review Required Before Drafting'),
  row('CLM-P2C-LAW-009','', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(a)(1)-(4)', 'Medium', 'Retired from pilot'),
  row('CLM-P2E-LAW-009A','CLM-P2C-LAW-009', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(a)(1)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-009B','CLM-P2C-LAW-009', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(a)(2)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-009C','CLM-P2C-LAW-009', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(a)(3)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2E-LAW-009D','CLM-P2C-LAW-009', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(a)(4)', 'Medium', 'Narrowed/Split Claim Created'),
  row('CLM-P2C-LAW-010','', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(b)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-011','', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(c)(3)(A)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-012','', 'Contract Requirements & Execution', URLs.u7159, 'BPC §7159(c)(5)', 'Medium', 'Legal Review Required Before Drafting'),
  row('CLM-P2C-LAW-013','', 'Business Finances / Payments', URLs.u71595, 'BPC §7159.5(a)(3), §7159.5(a)(8)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-014','', 'Business Finances / Payments', URLs.u71595, 'BPC §7159.5(a)(5), §7159.5(a)(8)', 'Medium', 'Drafting Candidate Later'),
  row('CLM-P2C-LAW-015','', 'Insurance & Liens', URLs.u8200, 'Civil Code §8200(a)-(e)', 'High', 'Legal Review Required Before Drafting')
];
