
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.wall_opening_engine import build_wall_openings

site=normalize_site({"width_m":20,"depth_m":30,
                     "setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 5 bedrooms, 2 floors, 3 parking")
bundle=generate_project(brief,site)

for project in bundle["alternatives"]:
    m=build_wall_openings(project)
    assert m["status"]=="SEGMENTED_ARCHITECTURAL_MODEL"
    assert m["counts"]["walls"]>0
    assert m["counts"]["doors"]>0
    assert m["counts"]["windows"]>0
    assert m["materials"]["external_wall"]=="Wall-External-250mm"
    assert any(x["category"].startswith("External/Internal") for x in m["boq"])
    assert any(x["category"]=="Door" for x in m["boq"])
print("ALL TAKWEEN v2.8 TESTS PASSED")
