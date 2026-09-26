
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.wall_opening_engine import build_wall_openings
from backend.opening_relationships import build_opening_relationships
from backend.materials_finishes import apply_materials
from backend.boq_engine import generate_boq

site=normalize_site({"width_m":20,"depth_m":30,"setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
bundle=generate_project(brief,site)
model=build_wall_openings(bundle["alternatives"][0])
model=apply_materials(model)
rels=build_opening_relationships(model)

assert rels["status"]=="OPENINGS_RELATIONSHIPS_READY"
assert rels["counts"]["openings"]==rels["counts"]["doors"]+rels["counts"]["windows"]
assert len(rels["relationships"])==rels["counts"]["openings"]*2
assert all("material" in x for x in model["elements"] if x["entity"] in ["IfcWall","IfcDoor","IfcWindow"])

project={"levels":bundle["alternatives"][0]["levels"],"elements":model["elements"]}
boq=generate_boq(project)
assert boq["boq_version"]=="0.2"
assert any(x["category"]=="Floor Finish" for x in boq["items"])
assert any(x["category"]=="Door" for x in boq["items"])
assert any(x["category"]=="Window" for x in boq["items"])
print("ALL TAKWEEN v2.9 TESTS PASSED")
