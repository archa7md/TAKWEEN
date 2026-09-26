
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.ifc_writer import export_ifc

site = normalize_site({"width_m":20,"depth_m":30,"setbacks":{"front":5,"rear":3,"left":2,"right":2}})
brief = parse_brief("Villa 4 bedrooms, 2 floors, 2 parking")
project = generate_project(brief, site)

with tempfile.TemporaryDirectory() as d:
    path = Path(d)/"villa.ifc"
    export_ifc(project, str(path))
    content = path.read_text(encoding="utf-8")
    assert content.startswith("ISO-10303-21;")
    assert "FILE_SCHEMA(('IFC4'));" in content
    assert "IFCPROJECT" in content
    assert "IFCSITE" in content
    assert "IFCBUILDING" in content
    assert "IFCBUILDINGSTOREY" in content
    assert "IFCSPACE" in content
    assert content.endswith("END-ISO-10303-21;\n")

print("ALL TAKWEEN v2.5 TESTS PASSED")
