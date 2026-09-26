from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .site_intelligence import normalize_site
from .ai_brief import parse_brief
from .architecture_engine import generate_project
from .site_rules import assess_rules
from .bim_schema import build_bim_model, build_physical_model
app=FastAPI(title='TAKWEEN | تكوين Architecture Platform API',version='FINAL-MVP-1.0')
class Brief(BaseModel): text:str
@app.get('/health')
def health(): return {'status':'ok','product':'TAKWEEN | تكوين','version':'FINAL-MVP-1.0','mode':'architect-review-required'}
@app.post('/ai/brief')
def ai(x:Brief): return parse_brief(x.text)
@app.post('/projects/analyze-site')
def site(x:dict):
 s=normalize_site(x); return {'site':s,'rules':assess_rules({'site':s['site']})}
@app.post('/projects/generate')
def gen(x:dict):
 s=normalize_site(x['site']); p=generate_project(x['brief'],s); p['site']=s['site']; p['rules']=assess_rules(p); return p
@app.post('/projects/bim')
def bim(x:dict): return build_bim_model(x)


@app.post("/projects/ifc-intermediate")
def ifc_intermediate(payload: dict):
    return build_physical_model(payload)


@app.post("/projects/export-ifc")
def export_ifc_endpoint(payload: dict):
    from .ifc_writer import export_ifc
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".ifc")
    os.close(fd)
    export_ifc(payload, path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    os.unlink(path)
    return {"filename":"TAKWEEN_generated.ifc","format":"IFC4","content":content}

@app.post("/projects/geometry")
def geometry_model(payload: dict):
    from .ifc_geometry import add_geometry
    return add_geometry(payload)

@app.post("/projects/boq")
def boq(payload: dict):
    from .boq_engine import generate_boq
    return generate_boq(payload)


@app.post("/projects/architectural-bim")
def architectural_bim(payload: dict):
    from .architectural_bim import build_architectural_bim
    return build_architectural_bim(payload)


@app.post("/projects/wall-openings")
def wall_openings(payload: dict):
    from .wall_opening_engine import build_wall_openings
    return build_wall_openings(payload)

@app.post("/projects/openings")
def openings(payload: dict):
    from .opening_relationships import build_opening_relationships
    return build_opening_relationships(payload)

@app.post("/projects/materials")
def materials(payload: dict):
    from .materials_finishes import apply_materials
    return apply_materials(payload)

@app.post("/projects/optimize")
def optimize_endpoint(payload: dict):
    from .optimization_engine import optimize
    return optimize(payload.get("alternatives",[]),payload.get("weights"))

@app.post("/projects/optimize-geometry")
def optimize_geometry(payload: dict):
    from .optimization_engine import optimize
    from .geometry_metrics import metrics
    return optimize(payload.get("alternatives",[]),payload.get("weights"),metrics)

# --- TAKWEEN v3.2 Constraint Solver ---

from constraint_solver import solve_alternative, SolveConfig
try:
    from fastapi import Body
    @app.post("/projects/solve")
    def solve_project_endpoint(payload: dict = Body(...)):
        alt = payload.get("alternative", payload)
        return solve_alternative(alt)
except Exception:
    pass

from space_arrangement_engine import arrangement_metrics, optimize_arrangement
try:
 from fastapi import Body
 @app.post("/projects/arrange")
 def arrange_project_endpoint(payload: dict = Body(...)):
  alt=payload.get("alternative",payload); solved,metrics=optimize_arrangement(alt); return {"alternative":solved,"metrics":metrics}
except Exception: pass

from multi_floor_engine import plan_multi_floor
try:
 from fastapi import Body
 @app.post("/projects/multi-floor-plan")
 def multi_floor_plan_endpoint(payload: dict = Body(...)):
  return plan_multi_floor(payload.get("alternative",payload))
except Exception:
 pass

from saudi_villa_intelligence import optimize_villa_intelligence
try:
 from fastapi import Body
 @app.post("/projects/saudi-villa-intelligence")
 def saudi_villa_endpoint(payload: dict = Body(...)):
  s,m=optimize_villa_intelligence(payload.get("alternative",payload)); return {"alternative":s,"metrics":m}
except Exception: pass

from unified_design_engine import unified_project_analysis
@app.post("/projects/unified-analysis")
def unified_analysis_endpoint(payload: dict): return unified_project_analysis(payload)

# --- TAKWEEN v3.8 AI Design Decision Layer ---
from design_decision_engine import analyze_alternative, design_decision
@app.post("/projects/design-decision")
def design_decision_endpoint(payload: dict):
    if isinstance(payload, dict) and ("alternative" in payload):
        return analyze_alternative(payload.get("alternative", {}), payload.get("weights"))
    return design_decision(payload, payload.get("weights") if isinstance(payload, dict) else None, payload.get("top_k", 6) if isinstance(payload, dict) else 6)

# --- TAKWEEN v3.9 Design Iteration Engine ---
from design_iteration_engine import iterate_alternative, iterate_project
@app.post("/projects/design-iteration")
def design_iteration_endpoint(payload: dict):
    if isinstance(payload, dict) and ("alternative" in payload):
        return iterate_alternative(payload.get("alternative", {}), payload.get("decision"), payload.get("weights"), payload.get("min_improvement", 0.0001))
    return iterate_project(payload, payload.get("weights") if isinstance(payload, dict) else None, payload.get("top_k", 6) if isinstance(payload, dict) else 6)

# --- TAKWEEN v4.0 Generative Design Engine ---
from generative_design_engine import generate_project as generate_design_alternatives
@app.post("/projects/generative-design")
def generative_design_endpoint(payload: dict):
    return generate_design_alternatives(payload, payload.get("weights") if isinstance(payload, dict) else None, payload.get("count", 8) if isinstance(payload, dict) else 8, payload.get("refine", True) if isinstance(payload, dict) else True)


# --- TAKWEEN Final MVP unified production pipeline ---
from production_pipeline import build_pipeline
from validation import validate_request, validate_result
from fastapi import HTTPException

@app.post("/projects/final-pipeline")
def final_pipeline(payload: dict):
    errors = validate_request(payload)
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    result = build_pipeline(payload)
    result["validation"] = validate_result(result)
    return result

@app.get("/platform/manifest")
def platform_manifest():
    return {
        "product":"TAKWEEN | تكوين",
        "version":"FINAL-MVP-1.0",
        "pipeline":["Brief","Site Intelligence","Architecture Generation","Generative Design","Unified Analysis","Design Decision","Design Iteration","BIM","BOQ","IFC"],
        "status":"MVP READY FOR ARCHITECT REVIEW",
        "not_yet_automated":["authoritative Saudi code verification","structural engineering","MEP engineering","production fire/life-safety analysis","commercial billing/authentication/cloud collaboration"]
    }


@app.get("/", include_in_schema=False)
def web_app():
    return FileResponse("frontend/index.html")
