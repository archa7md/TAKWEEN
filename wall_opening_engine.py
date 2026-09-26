
from typing import Dict, Any, List

EXT_T=0.25
INT_T=0.20
H=3.20

def rect(room):
    g=room.get("geometry",{})
    return float(g.get("x",0)),float(g.get("y",0)),float(g.get("w",3)),float(g.get("h",3))

def wall_segments(room, level_name, external=False):
    x,y,w,d=rect(room)
    t=EXT_T if external else INT_T
    kind="external" if external else "internal"
    return [
        {"entity":"IfcWall","id":f"{kind[:3].upper()}-N-{room['id']}","type":kind,
         "level":level_name,"axis":"X","x":x,"y":y,"length_m":w,"height_m":H,"thickness_m":t},
        {"entity":"IfcWall","id":f"{kind[:3].upper()}-S-{room['id']}","type":kind,
         "level":level_name,"axis":"X","x":x,"y":y+d,"length_m":w,"height_m":H,"thickness_m":t},
        {"entity":"IfcWall","id":f"{kind[:3].upper()}-W-{room['id']}","type":kind,
         "level":level_name,"axis":"Y","x":x,"y":y,"length_m":d,"height_m":H,"thickness_m":t},
        {"entity":"IfcWall","id":f"{kind[:3].upper()}-E-{room['id']}","type":kind,
         "level":level_name,"axis":"Y","x":x+w,"y":y,"length_m":d,"height_m":H,"thickness_m":t}
    ]

def build_wall_openings(project:Dict[str,Any])->Dict[str,Any]:
    elements=[]; boq=[]
    for level in project.get("levels",[]):
        rooms=level.get("rooms",[])
        for idx,room in enumerate(rooms):
            x,y,w,d=rect(room)
            # First room per level treated as core/internal; others receive external envelope candidates.
            external=(idx>0)
            elements.extend(wall_segments(room,level.get("name"),external))
            elements.append({
                "entity":"IfcDoor","id":f"DOOR-{room['id']}","host":room["id"],
                "width_m":0.90,"height_m":2.10,"swing":"inward",
                "placement":{"x":x+0.15,"y":y,"z":float(level.get("elevation_m",0))}
            })
            if external:
                elements.append({
                    "entity":"IfcWindow","id":f"WIN-{room['id']}","host":room["id"],
                    "width_m":1.50,"height_m":1.40,"sill_height_m":0.90,
                    "placement":{"x":x+w/2-0.75,"y":y,"z":float(level.get("elevation_m",0))+0.90}
                })
            perimeter=2*(w+d)
            wall_area=perimeter*H
            boq.append({"category":"External/Internal Walls",
                        "description":room["name"],"unit":"m2",
                        "quantity":round(wall_area,2),
                        "basis":"segmented wall lengths"})
            boq.append({"category":"Door","description":room["name"],
                        "unit":"item","quantity":1})
            if external:
                boq.append({"category":"Window","description":room["name"],
                            "unit":"item","quantity":1})
    return {
        "schema":"TAKWEEN-WALL-OPENINGS-2.8",
        "status":"SEGMENTED_ARCHITECTURAL_MODEL",
        "elements":elements,
        "boq":boq,
        "materials":{
            "external_wall":"Wall-External-250mm",
            "internal_wall":"Wall-Internal-200mm",
            "door":"Door-900x2100",
            "window":"Window-1500x1400"
        },
        "counts":{
            "walls":sum(x["entity"]=="IfcWall" for x in elements),
            "doors":sum(x["entity"]=="IfcDoor" for x in elements),
            "windows":sum(x["entity"]=="IfcWindow" for x in elements)
        }
    }
