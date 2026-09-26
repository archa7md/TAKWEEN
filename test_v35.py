import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from saudi_villa_intelligence import villa_metrics,optimize_villa_intelligence

def test():
 a={"rooms":[{"name":"Entrance","x":0,"y":0,"w":2,"h":2},{"name":"Majlis","x":2,"y":0,"w":4,"h":4},{"name":"Family Living","x":8,"y":6,"w":4,"h":4},{"name":"Master Bedroom","x":8,"y":0,"w":4,"h":4},{"name":"Kitchen","x":5,"y":6,"w":3,"h":3}]}
 m=villa_metrics(a); assert m["saudi_villa_score"]>=0
 s,_=optimize_villa_intelligence({"rooms":[{"name":"Majlis"},{"name":"Family Living"},{"name":"Kitchen"},{"name":"Master Bedroom"}]})
 z={r["name"]:r["design_zone"] for r in s["rooms"]}
 assert z=={"Majlis":"guest","Family Living":"family","Kitchen":"service","Master Bedroom":"family"}
 s,_=optimize_villa_intelligence({"rooms":[{"name":"Majlis","zone_locked":True,"design_zone":"custom"}]})
 assert s["rooms"][0]["design_zone"]=="custom"
 print("ALL TAKWEEN v3.5 TESTS PASSED")
if __name__=="__main__": test()
