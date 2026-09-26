import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from design_iteration_engine import iterate_alternative, iterate_project


def test():
    a={"site_fit":{"width_m":20,"depth_m":30},"levels":[{"name":"Ground","rooms":[
        {"name":"Entrance / Foyer","geometry":{"x":1,"y":1,"w":3,"h":3}},
        {"name":"Majlis","geometry":{"x":4,"y":1,"w":5,"h":4}},
        {"name":"Kitchen","geometry":{"x":4,"y":7,"w":4,"h":4}},
        {"name":"Dining","geometry":{"x":12,"y":7,"w":4,"h":4}},
        {"name":"Master Bedroom","geometry":{"x":4,"y":4,"w":5,"h":4}},
    ]}]}
    r=iterate_alternative(a)
    assert r["version"]=="3.9"
    assert r["status"] in {"improved","no_improvement"}
    assert 0<=r["before"]["score"]<=1 and 0<=r["after"]["score"]<=1
    assert r["candidate_count"]>=1
    assert r["alternative"]
    p=iterate_project({"alternatives":[a,dict(a)]})
    assert p["alternatives_count"]==2 and len(p["iterations"])==2
    print("ALL TAKWEEN v3.9 TESTS PASSED")
if __name__=="__main__": test()
