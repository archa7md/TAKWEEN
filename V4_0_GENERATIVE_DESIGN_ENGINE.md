# TAKWEEN v4.0 — Generative Design Engine

## Purpose
Generate multiple deterministic architectural alternatives from a parametric base alternative, evaluate them with the v3.7 Unified Design Intelligence layer, and optionally refine each candidate using v3.9 Design Iteration.

## Strategies
- baseline
- mirror_x / mirror_y
- compact / expanded
- public_front / private_back
- bounded translations

## Pipeline
`Base Alternative → Candidate Generation → v3.7 Scoring → Ranking → v3.9 Refinement → Before/After Trace`

## Important limitation
This version is **generative by parametric transformation**, not an LLM and not a global optimization solver. It does not claim Saudi Building Code or municipality compliance, solar simulation, or final design approval.
