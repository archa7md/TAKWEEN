# TAKWEEN | تكوين — Final MVP 1.0

**From Brief to BIM | من الفكرة إلى BIM**

## What is included
- Natural-language project brief parsing (deterministic local adapter).
- Site and buildable-envelope normalization.
- Parametric architecture starter generation.
- Generative design alternatives (bounded deterministic engine).
- Unified geometry / adjacency / privacy / efficiency / orientation / multi-floor analysis.
- Explainable design decision layer.
- Design iteration with before/after impact.
- Architectural BIM intermediate model.
- Physical IFC-intermediate model.
- IFC4 text export foundation.
- Preliminary BOQ.
- Arabic RTL browser MVP.
- FastAPI API + Docker packaging.
- Regression tests across the development stack.

## One-call workflow
`POST /projects/final-pipeline`

The response contains the brief, site analysis, generated alternatives, analysis, decisions, iterations, selected alternative, BIM, physical BIM, BOQ and IFC text.

## Run
```bash
pip install -r backend/requirements.txt
./run.sh
```
Then open `/docs` for the API or `/frontend/index.html` through a static server. For Docker:
```bash
docker build -t takween .
docker run -p 8000:8000 takween
```

## Important production boundaries
This is a **production-oriented MVP**, not a legally compliant automated architect.
- Saudi Building Code / municipality rules must be connected to authoritative, jurisdiction-specific, versioned sources and professionally verified.
- Structural, MEP, fire/life-safety, accessibility and energy checks are not complete production engineering modules.
- Solar/daylight/orientation are transparent heuristics, not simulation.
- Geometry is simplified rectangular prototype geometry.
- BOQ is design-stage preliminary quantity information.
- IFC is an interoperability foundation and should be validated in Revit/IFC software.
- No cloud authentication, billing, multi-user collaboration or managed database is included in this local MVP.
- Human architect review remains mandatory.
