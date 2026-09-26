import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.ifc_geometry import add_geometry
from backend.boq_engine import generate_boq
site=normalize_site({"width_m":20,"depth_m":30,"setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
bundle=generate_project(brief,site)
assert len(bundle["alternatives"])==6
for project in bundle["alternatives"]:
    project=add_geometry(project)
    rooms=[r for l in project["levels"] for r in l["rooms"]]
    assert rooms and all(r["geometry_3d"]["type"]=="IfcExtrudedAreaSolid" for r in rooms)
    boq=generate_boq(project)
    assert boq["status"]=="PRELIMINARY" and len(boq["items"])>0
print("ALL TAKWEEN v2.6 TESTS PASSED")
