# TAKWEEN Production v3.8

AI Design Decision Layer on top of v3.7 Unified Design Intelligence.

### Added
- Explainable architectural decision states: retain / revise / review
- Strengths and issues grounded in measurable factors
- Actionable architectural recommendations
- Factor and metric traceability
- Confidence and explicit limitations
- API endpoint: `/projects/design-decision`
- JSON output schema
- Automated regression test

Run:
`pip install -r backend/requirements.txt`
`uvicorn backend.main:app --reload`
`python tests/test_v38.py`
