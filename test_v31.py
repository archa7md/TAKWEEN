
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.geometry_metrics import metrics
from backend.optimization_engine import optimize
site=normalize_site({"width_m":20,"depth_m":30,"setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
alts=generate_project(brief,site)["alternatives"]
m=metrics(alts[0])
assert all(k in m for k in ["area_efficiency","circulation","privacy","daylight","adjacency","envelope_fit"])
assert all(0<=m[k]<=1 for k in ["area_efficiency","circulation","privacy","daylight","adjacency","envelope_fit"])
r=optimize(alts,{"privacy":.4,"efficiency":.3,"circulation":.2,"daylight":.1},metrics)
assert r["mode"]=="geometry-based" and len(r["alternatives"])==6
assert all("geometry_metrics" in x for x in r["alternatives"])
print("ALL TAKWEEN v3.1 TESTS PASSED")
