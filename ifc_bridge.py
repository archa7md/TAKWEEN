
from typing import Dict, Any, List

IFC_SCHEMA = "IFC4"

def _wall(space, thickness=0.20):
    g = space.get("geometry", {})
    return {
        "entity": "IfcWall",
        "id": f"WALL-{space['id']}",
        "space_id": space["id"],
        "thickness_m": thickness,
        "geometry": {"x":g.get("x",0),"y":g.get("y",0),"w":g.get("w",0),"h":g.get("h",0)}
    }

def _opening(space, kind):
    g = space.get("geometry", {})
    return {
        "entity": "IfcDoor" if kind=="door" else "IfcWindow",
        "id": f"{kind.upper()}-{space['id']}",
        "space_id": space["id"],
        "geometry": {
            "host_x": g.get("x",0),
            "host_y": g.get("y",0),
            "width_m": 0.90 if kind=="door" else 1.50,
            "height_m": 2.10 if kind=="door" else 1.40
        }
    }

def build_ifc_intermediate(project: Dict[str, Any]) -> Dict[str, Any]:
    walls, doors, windows, slabs, stairs = [], [], [], [], []
    levels = project.get("levels", [])
    if not levels and project.get("alternatives"):
        levels = project["alternatives"][0].get("levels", [])

    for level in levels:
        rooms = level.get("rooms", [])
        slabs.append({
            "entity":"IfcSlab",
            "id":f"SLAB-{level.get('name','LEVEL').replace(' ','-')}",
            "level":level.get("name"),
            "elevation_m":level.get("elevation_m",0),
            "thickness_m":0.20,
            "area_m2": round(sum(float(r.get("geometry",{}).get("w",0))*float(r.get("geometry",{}).get("h",0)) for r in rooms),2)
        })
        for room in rooms:
            walls.append(_wall(room))
            doors.append(_opening(room, "door"))
            windows.append(_opening(room, "window"))

    if len(levels) > 1:
        stairs.append({
            "entity":"IfcStair",
            "id":"STAIR-MAIN",
            "levels":[l.get("name") for l in levels],
            "width_m":1.20,
            "status":"PRELIMINARY"
        })

    return {
        "schema":"IFC4",
        "bridge_version":"0.1",
        "status":"IFC_INTERMEDIATE_READY",
        "levels": levels,
        "elements":{
            "walls":walls,
            "doors":doors,
            "windows":windows,
            "slabs":slabs,
            "stairs":stairs
        },
        "export_note":"Geometry is normalized intermediate data; a native IFC writer is the next step."
    }
