import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production_pipeline import build_pipeline
from validation import validate_request, validate_result

def test_final():
    payload={"brief_text":"فيلا دورين، 5 غرف نوم، مجلس ضيوف، صالة عائلية، مطبخ، سفرة، 2 مواقف", "count":4,
             "site":{"width_m":20,"depth_m":30,"north_deg":0}}
    assert validate_request(payload)==[]
    r=build_pipeline(payload)
    v=validate_result(r)
    assert v["valid"]
    assert r["version"]=="FINAL-MVP-1.0"
    assert len(r["generative_design"]["results"])==4
    assert r["ifc"]["format"]=="IFC4"
    assert r["boq"]["status"]=="PRELIMINARY"
    assert r["bim"]["schema_id"].startswith("TAKWEEN-BIM")
    print("ALL TAKWEEN FINAL PIPELINE TESTS PASSED")

if __name__=="__main__": test_final()
