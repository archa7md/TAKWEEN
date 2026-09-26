# TAKWEEN v3.2 — Constraint Solver

v3.2 moves TAKWEEN from **layout evaluation** toward **automatic layout refinement**.

## What was added
- Deterministic bounded local-search solver.
- Room translation and dimension candidates.
- Hard checks for envelope, overlap, minimum area and minimum dimensions.
- Before/after score and constraint report.
- Solver metadata embedded in the result.
- `/projects/solve` FastAPI endpoint when the existing API entrypoint is detected.
- Regression tests.

## Important limitation
This is an architectural optimization foundation, not a global optimizer. It does not guarantee the mathematically optimal plan. Saudi code, fire, accessibility, structural and MEP compliance remain REVIEW items until connected to authoritative, versioned rule sources and production-grade solvers.
