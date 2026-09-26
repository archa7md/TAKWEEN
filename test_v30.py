
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.optimization_engine import optimize
site=normalize_site({"width_m":20,"depth_m":30,"setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
alts=generate_project(brief,site)["alternatives"]
r=optimize(alts)
assert len(r["alternatives"])==6
assert [x["optimization"]["rank"] for x in r["alternatives"]]==list(range(1,7))
assert abs(sum(r["weights"].values())-1)<.001
p=optimize(alts,{"privacy":1,"adjacency":0,"circulation":0,"efficiency":0,"orientation":0,"parking":0,"daylight":0})
assert p["alternatives"][0]["optimization"]["factors"]["privacy"]>=.72
print("ALL TAKWEEN v3.0 TESTS PASSED")
