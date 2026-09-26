# TAKWEEN v3.9 — Design Iteration Engine

## Purpose
v3.9 closes the loop between the v3.8 explainable decision layer and actual design geometry. It takes weak factors, generates bounded deterministic edits, re-runs the v3.7 unified analysis, and reports the before/after effect.

## Flow
`Unified Analysis → Decision Layer → Candidate Edit → Constraint Check → Re-score → Before/After Impact`

## API
`POST /projects/design-iteration`

Payload can contain `alternative`, optional `decision`, and optional `weights`.
For multiple alternatives use `alternatives` and optional `decisions`.

## Output
- `status`: `improved` or `no_improvement`
- before/after score and components
- `score_delta`
- selected factor and candidate list
- constraint status
- trace of weak factors, weights, and threshold

## Safety of the prototype
The engine uses bounded deterministic edits. It does not claim a global optimum, code compliance, solar simulation, or final architectural approval. Architect review remains required.
