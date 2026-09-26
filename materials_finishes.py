
from typing import Dict, Any

MATERIALS={
    "external_wall":"External Plaster / Paint",
    "internal_wall":"Gypsum / Paint",
    "floor":"Porcelain / Stone Finish",
    "ceiling":"Gypsum Board",
    "door":"Painted Timber / Veneer",
    "window":"Bronze Aluminum + Glass"
}

def apply_materials(model:Dict[str,Any])->Dict[str,Any]:
    for e in model.get("elements",[]):
        typ=e.get("entity")
        if typ=="IfcWall":
            e["material"]=MATERIALS["external_wall"] if e.get("type")=="external" else MATERIALS["internal_wall"]
        elif typ=="IfcDoor": e["material"]=MATERIALS["door"]
        elif typ=="IfcWindow": e["material"]=MATERIALS["window"]
        elif typ=="IfcSlab": e["finish"]=MATERIALS["floor"]
    model["materials"]=MATERIALS
    return model
