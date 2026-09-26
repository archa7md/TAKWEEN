import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from generative_design_engine import generate_alternatives, generate_project

def test():
    a={"site_fit":{"width_m":20,"depth_m":30},"levels":[{"name":"Ground","rooms":[
        {"name":"Entrance / Foyer","geometry":{"x":1,"y":1,"w":3,"h":3}},
        {"name":"Majlis","geometry":{"x":4,"y":1,"w":5,"h":4}},
        {"name":"Kitchen","geometry":{"x":4,"y":7,"w":4,"h":4}},
        {"name":"Dining","geometry":{"x":12,"y":7,"w":4,"h":4}},
        {"name":"Master Bedroom","geometry":{"x":4,"y":4,"w":5,"h":4}}
    ]}]}
    g=generate_alternatives(a,9)
    assert len(g)>=6
    p=generate_project({"alternatives":[a]},count=8,refine=True)
    assert p["version"]=="4.0"
    assert p["generated_count"]==8
    assert len(p["results"])==8
    assert all(0<=x["score"]<=1 for x in p["results"])
    assert all("strategy" in x and "components" in x for x in p["results"])
    print("ALL TAKWEEN v4.0 TESTS PASSED")
if __name__=="__main__": test()
