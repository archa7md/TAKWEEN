
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from constraint_solver import solve_alternative, SolveConfig

def score(a):
    # Higher is better: fewer violations, then prefer compact coordinates.
    rooms=a["rooms"]
    violations=0
    for i,x in enumerate(rooms):
        for y in rooms[i+1:]:
            ax,ay,aw,ah=x["x"],x["y"],x["w"],x["h"]
            bx,by,bw,bh=y["x"],y["y"],y["w"],y["h"]
            if max(0,min(ax+aw,bx+bw)-max(ax,bx))*max(0,min(ay+ah,by+bh)-max(ay,by)) > 0:
                violations += 1
    return -100*violations - sum((r["x"]+r["y"])*0.001 for r in rooms)

def test_solver_reduces_overlap():
    alt={
        "envelope":{"width_m":12,"depth_m":10},
        "rooms":[
            {"name":"Living","x":0,"y":0,"w":5,"h":4,"min_area_m2":12,"min_width_m":3},
            {"name":"Majlis","x":4,"y":0,"w":5,"h":4,"min_area_m2":12,"min_width_m":3},
            {"name":"Kitchen","x":0,"y":4,"w":3,"h":3,"min_area_m2":6,"min_width_m":2},
        ]
    }
    solved, report=solve_alternative(alt, scorer=score, config=SolveConfig(iterations=80,step_m=.5,size_step_m=.25))
    assert report["after_score"] >= report["before_score"]
    assert len(report["after_violations"]) <= len(report["before_violations"])

def test_constraints_preserved():
    alt={
        "envelope":{"width_m":10,"depth_m":8},
        "rooms":[
            {"name":"A","x":0,"y":0,"w":3,"h":3,"min_area_m2":9,"min_width_m":2},
            {"name":"B","x":3,"y":0,"w":3,"h":3,"min_area_m2":9,"min_width_m":2},
        ]
    }
    solved, report=solve_alternative(alt, scorer=score, config=SolveConfig(iterations=30))
    for r in solved["rooms"]:
        assert r["w"]*r["h"] >= r["min_area_m2"]
        assert r["w"] >= r["min_width_m"]

def test_metadata():
    alt={"envelope":{"width_m":8,"depth_m":8},"rooms":[{"name":"A","x":0,"y":0,"w":2,"h":2}]}
    solved,_=solve_alternative(alt, scorer=score)
    assert solved["solver_v3_2"]["method"]=="deterministic_bounded_local_search"

if __name__=="__main__":
    test_solver_reduces_overlap()
    test_constraints_preserved()
    test_metadata()
    print("ALL TAKWEEN v3.2 TESTS PASSED")
