import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from design_decision_engine import analyze_alternative, design_decision


def test():
    a = {
        "rooms": [
            {"name": "Entrance", "x": 8, "y": 2, "w": 2, "h": 2},
            {"name": "Majlis", "x": 1, "y": 3, "w": 5, "h": 4},
            {"name": "Family Living", "x": 10, "y": 8, "w": 6, "h": 5},
            {"name": "Master Bedroom", "x": 10, "y": 20, "w": 5, "h": 5},
            {"name": "Kitchen", "x": 4, "y": 9, "w": 4, "h": 4}
        ],
        "site": {"width_m": 20, "depth_m": 30, "road_sides": ["south"], "view_sides": ["north"]},
        "floors": 2
    }
    r = analyze_alternative(a)
    assert r["version"] == "3.8"
    assert r["decision"] in {"retain", "revise", "review"}
    assert 0 <= r["score"] <= 1
    assert r["factor_trace"] and r["source_metrics"]["components"]
    assert isinstance(r["recommended_actions"], list)
    p = design_decision({"alternatives": [a, dict(a)]})
    assert p["alternatives_count"] == 2
    assert len(p["decisions"]) == 2
    print("ALL TAKWEEN v3.8 TESTS PASSED")

if __name__ == "__main__":
    test()
