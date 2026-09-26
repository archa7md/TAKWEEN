"""TAKWEEN Final MVP production pipeline.

Orchestrates the deterministic architecture stack from brief/site to generated
alternatives, explainable decisions, iteration, BIM, BOQ and IFC text export.
It is deliberately explicit about review-only stages and never claims legal/code
compliance from heuristic rules.
"""
from copy import deepcopy
from backend.ai_brief import parse_brief
from backend.site_intelligence import normalize_site
from backend.architecture_engine import generate_project
from generative_design_engine import generate_project as generate_design
from unified_design_engine import unified_project_analysis
from design_decision_engine import design_decision
from design_iteration_engine import iterate_project
from backend.bim_schema import build_bim_model, build_physical_model
from backend.boq_engine import generate_boq
from backend.ifc_writer import export_ifc
import tempfile, os

FINAL_VERSION = "FINAL-MVP-1.0"

def build_pipeline(payload: dict) -> dict:
    payload = payload or {}
    brief_text = payload.get("brief_text") or payload.get("brief")
    if isinstance(brief_text, dict):
        brief = deepcopy(brief_text)
    else:
        brief = parse_brief(str(brief_text or ""))
    site = normalize_site(payload.get("site") or {})
    generated_base = generate_project(brief, site)
    count = max(1, min(int(payload.get("count", 8)), 12))
    generated = generate_design({"alternatives": generated_base["alternatives"]}, payload.get("weights"), count, True)
    alternatives = [r.get("refined_alternative") or r["alternative"] for r in generated["results"]]
    unified = unified_project_analysis({"alternatives": alternatives}, payload.get("weights"), min(6, len(alternatives)))
    decisions = design_decision({"alternatives": alternatives}, payload.get("weights"), min(6, len(alternatives)))
    iterations = iterate_project({"alternatives": alternatives}, payload.get("weights"), min(6, len(alternatives)))
    chosen = alternatives[0] if alternatives else {}
    bim = build_bim_model(chosen)
    physical = build_physical_model(chosen)
    boq = generate_boq(physical)
    # IFC writer accepts the physical model; return IFC as text for API portability.
    fd, path = tempfile.mkstemp(suffix=".ifc"); os.close(fd)
    try:
        export_ifc(physical, path)
        with open(path, "r", encoding="utf-8") as f: ifc_text = f.read()
    finally:
        try: os.unlink(path)
        except OSError: pass
    return {
        "product":"TAKWEEN | تكوين", "version":FINAL_VERSION,
        "status":"READY_FOR_ARCHITECT_REVIEW",
        "brief":brief, "site":site,
        "base_generation":generated_base,
        "generative_design":generated,
        "unified_analysis":unified,
        "decisions":decisions,
        "iterations":iterations,
        "selected_alternative":chosen,
        "bim":bim, "physical_bim":physical, "boq":boq,
        "ifc":{"format":"IFC4","status":"GENERATED_TEXT","content":ifc_text},
        "review_flags":[
            "Saudi code/municipality rules require jurisdiction-specific authoritative sources and professional verification.",
            "Structural, MEP, fire/life-safety, accessibility and energy compliance are not fully automated.",
            "Geometry, daylight and orientation are prototype/heuristic calculations.",
            "BOQ is preliminary design-stage quantity information, not a tender BOQ.",
            "IFC is a generated interoperability foundation and should be validated in the target BIM platform."
        ]
    }
