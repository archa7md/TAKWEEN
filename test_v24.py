
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.ifc_bridge import build_ifc_intermediate

site = normalize_site({"width_m":20,"depth_m":30,"north_deg":0,
                       "setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief = parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
project = generate_project(brief, site)

physical = build_ifc_intermediate(project)

assert physical["schema"] == "IFC4"
assert physical["status"] == "IFC_INTERMEDIATE_READY"
assert len(physical["elements"]["walls"]) > 0
assert len(physical["elements"]["doors"]) == len(physical["elements"]["walls"])
assert len(physical["elements"]["windows"]) == len(physical["elements"]["walls"])
assert len(physical["elements"]["slabs"]) == 2
assert len(physical["elements"]["stairs"]) == 1

print("ALL TAKWEEN v2.4 TESTS PASSED")
