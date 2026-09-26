import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unified_design_engine import score_alternative,unified_project_analysis
def test():
 a={"rooms":[{"name":"Entrance"},{"name":"Majlis"},{"name":"Family Living"},{"name":"Master Bedroom"},{"name":"Kitchen"}],"site":{"width_m":20,"depth_m":30,"road_sides":["south"],"view_sides":["north"]},"floors":2}
 r=score_alternative(a); assert 0<=r["score"]<=1 and len(r["components"])==7
 p=unified_project_analysis({"alternatives":[a,dict(a)]}); assert len(p["ranked_alternatives"])==2 and p["ranked_alternatives"][0]["unified_design_intelligence_v3_7"]["rank"]==1
 print("ALL TAKWEEN v3.7 TESTS PASSED")
if __name__=="__main__": test()
