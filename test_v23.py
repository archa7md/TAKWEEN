import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.site_intelligence import normalize_site
from backend.ai_brief import parse_brief
from backend.architecture_engine import generate_project
from backend.site_rules import assess_rules
from backend.bim_schema import build_bim_model
s=normalize_site({'width_m':20,'depth_m':30,'north_deg':90,'setbacks':{'front':5,'rear':3,'left':2,'right':2}}); assert s['derived']['buildable_width_m']==16 and s['derived']['buildable_depth_m']==22
b=parse_brief('فيلا 5 غرف نوم، دورين، 3 مواقف في جدة'); assert b['requirements']['bedrooms']==5 and b['requirements']['floors']==2 and b['requirements']['parking']==3
p=generate_project(b,s); assert len(p['alternatives'])==6
assert assess_rules({'site':s['site'],'program':b['requirements']})['registry_version']
assert len(build_bim_model(p)['spaces'])>0
print('ALL TAKWEEN v2.3 TESTS PASSED')
