
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.architectural_bim import build_architectural_bim

site=normalize_site({"width_m":20,"depth_m":30,
                     "setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief=parse_brief("Villa 5 bedrooms, 2 floors, 3 parking")
bundle=generate_project(brief,site)

assert len(bundle["alternatives"])==6

for project in bundle["alternatives"]:
    bim=build_architectural_bim(project)
    c=bim["counts"]
    assert c["spaces"]>0
    assert c["walls"]==c["spaces"]
    assert c["doors"]==c["spaces"]
    assert c["windows"]>0
    assert c["slabs"]==2
    assert c["stairs"]==1
    assert len(bim["boq"])>0
    assert any(x["category"]=="Floor Finish" for x in bim["boq"])
    assert any(x["category"]=="Internal Walls" for x in bim["boq"])
    assert any(x["category"]=="Paint" for x in bim["boq"])

print("ALL TAKWEEN v2.7 TESTS PASSED")
