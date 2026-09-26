
from typing import Dict, Any, List

WALL_T = 0.20
EXT_WALL_T = 0.25
FLOOR_H = 3.20

def _rect(room):
    g=room.get("geometry",{})
    return float(g.get("x",0)), float(g.get("y",0)), float(g.get("w",3)), float(g.get("h",3))

def build_architectural_bim(project: Dict[str,Any]) -> Dict[str,Any]:
    elements=[]
    boq=[]
    for li,level in enumerate(project.get("levels",[])):
        level_name=level.get("name",f"Level {li+1}")
        elevation=float(level.get("elevation_m",li*FLOOR_H))
        rooms=level.get("rooms",[])

        # Floor/slab
        slab_area=0
        for room in rooms:
            x,y,w,d=_rect(room)
            slab_area += w*d
            # Space
            elements.append({
                "entity":"IfcSpace","id":room.get("id"),
                "name":room.get("name"),"level":level_name,
                "placement":{"x":x,"y":y,"z":elevation},
                "dimensions":{"width":w,"depth":d,"height":FLOOR_H},
                "area_m2":round(w*d,2)
            })

            # Internal wall perimeter
            perimeter=2*(w+d)
            elements.append({
                "entity":"IfcWall","id":f"INTW-{room.get('id')}",
                "type":"internal","level":level_name,
                "thickness_m":WALL_T,"height_m":FLOOR_H,
                "length_m":round(perimeter,2)
            })

            # Door at room entry
            elements.append({
                "entity":"IfcDoor","id":f"DOOR-{room.get('id')}",
                "host_space":room.get("id"),"level":level_name,
                "width_m":0.90,"height_m":2.10,
                "placement":{"x":x,"y":y,"z":elevation}
            })

            # Window allowance on external-facing rooms
            if room.get("name","").lower() not in ["entrance / foyer","foyer"]:
                elements.append({
                    "entity":"IfcWindow","id":f"WIN-{room.get('id')}",
                    "host_space":room.get("id"),"level":level_name,
                    "width_m":1.50,"height_m":1.40,
                    "sill_height_m":0.90,
                    "placement":{"x":x,"y":y+d/2,"z":elevation+0.90}
                })

            boq += [
                {"category":"Floor Finish","description":room.get("name","Room"),
                 "unit":"m2","quantity":round(w*d,2)},
                {"category":"Internal Walls","description":room.get("name","Room"),
                 "unit":"m2","quantity":round(perimeter*FLOOR_H,2)},
                {"category":"Paint","description":room.get("name","Room"),
                 "unit":"m2","quantity":round(perimeter*FLOOR_H*2,2)}
            ]

        elements.append({
            "entity":"IfcSlab","id":f"SLAB-{li+1}",
            "level":level_name,"elevation_m":elevation,
            "thickness_m":0.20,"area_m2":round(slab_area,2)
        })
        boq.append({
            "category":"Concrete Slab","description":level_name,
            "unit":"m2","quantity":round(slab_area,2)
        })

    # Main stair if multiple floors
    if len(project.get("levels",[]))>1:
        elements.append({
            "entity":"IfcStair","id":"STAIR-MAIN",
            "width_m":1.20,"riser_m":0.17,"tread_m":0.29,
            "status":"PRELIMINARY"
        })
        boq.append({
            "category":"Stair","description":"Main stair",
            "unit":"item","quantity":1
        })

    return {
        "schema":"TAKWEEN-ARCH-BIM-2.7",
        "status":"ARCHITECTURAL_BIM_INTERMEDIATE",
        "elements":elements,
        "boq":boq,
        "counts":{
            "spaces":sum(1 for x in elements if x["entity"]=="IfcSpace"),
            "walls":sum(1 for x in elements if x["entity"]=="IfcWall"),
            "doors":sum(1 for x in elements if x["entity"]=="IfcDoor"),
            "windows":sum(1 for x in elements if x["entity"]=="IfcWindow"),
            "slabs":sum(1 for x in elements if x["entity"]=="IfcSlab"),
            "stairs":sum(1 for x in elements if x["entity"]=="IfcStair")
        }
    }
