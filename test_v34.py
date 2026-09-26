import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from multi_floor_engine import optimize_floors,vertical_demand,plan_multi_floor

def test():
 a={"floors":2,"envelope":{"width_m":12,"depth_m":10},"rooms":[
 {"name":"Majlis","floor":1},{"name":"Entrance","floor":1},
 {"name":"Master Bedroom","floor":0},{"name":"Bedroom 2","floor":0},
 {"name":"Kitchen","floor":0},{"name":"Dining","floor":0}]}
 before=vertical_demand(a)["vertical_demand"]; s=optimize_floors(a)
 assert vertical_demand(s)["vertical_demand"]<=before
 assert s["stair"]["width_m"]>0
 assert "0" in s["multi_floor_v3_4"]["floor_distribution"]
 b={"floors":2,"rooms":[{"name":"Master Bedroom","floor":0,"floor_locked":True}]}
 assert optimize_floors(b)["rooms"][0]["floor"]==0
 assert "alternative" in plan_multi_floor(b)
 print("ALL TAKWEEN v3.4 TESTS PASSED")
if __name__=="__main__": test()
