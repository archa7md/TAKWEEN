# TAKWEEN v3.8 — AI Design Decision Layer

## Purpose
v3.8 adds an explainable decision layer above the v3.7 Unified Design Intelligence engine.
It converts numeric component results into:

- decision state: `retain`, `revise`, or `review`
- strengths
- issues
- recommended architectural actions
- factor-by-factor trace
- confidence and limitations

## Important
This is a deterministic decision-support layer, not a real LLM. It does not claim Saudi Building Code or municipality compliance.

## API
`POST /projects/design-decision`

A single alternative can be sent as:
```json
{"alternative": {"rooms": [], "site": {}, "floors": 2}}
```

Multiple alternatives can be sent as:
```json
{"alternatives": [{"rooms": []}, {"rooms": []}], "top_k": 6}
```

Optional custom weights are accepted using the same v3.7 factor names.

## Decision logic
- `retain`: strong aggregate score with few weak factors and no detected hard geometry issues.
- `revise`: moderate score or identifiable weak factors that have actionable design improvements.
- `review`: low score or detected hard geometry issues requiring architect review.

These are workflow states, not architectural approval ratings.

## Next step
Future versions can replace the deterministic explanation generator with an LLM adapter while preserving the same structured output contract and traceability requirements.
