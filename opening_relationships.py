
from typing import Dict, Any

def build_opening_relationships(model: Dict[str,Any]) -> Dict[str,Any]:
    elements=model.get("elements",[])
    walls=[x for x in elements if x.get("entity")=="IfcWall"]
    doors=[x for x in elements if x.get("entity")=="IfcDoor"]
    windows=[x for x in elements if x.get("entity")=="IfcWindow"]

    relationships=[]
    openings=[]
    for opening_host in doors+windows:
        host=opening_host.get("host")
        if not host:
            # fallback to host_space -> nearest room wall id
            host_space=opening_host.get("host_space")
            host=f"INT-{host_space}" if host_space else None
        opening_id=f"OPENING-{opening_host['id']}"
        openings.append({
            "entity":"IfcOpeningElement",
            "id":opening_id,
            "host_element":host,
            "width_m":opening_host.get("width_m",0),
            "height_m":opening_host.get("height_m",0),
            "depth_m":0.25
        })
        relationships.append({
            "entity":"IfcRelVoidsElement",
            "id":f"REL-VOID-{opening_host['id']}",
            "relating_wall":host,
            "opening":opening_id
        })
        relationships.append({
            "entity":"IfcRelFillsElement",
            "id":f"REL-FILL-{opening_host['id']}",
            "opening":opening_id,
            "filling_element":opening_host["id"]
        })

    return {
        "schema":"TAKWEEN-OPENINGS-2.9",
        "status":"OPENINGS_RELATIONSHIPS_READY",
        "openings":openings,
        "relationships":relationships,
        "counts":{
            "walls":len(walls),"doors":len(doors),"windows":len(windows),
            "openings":len(openings)
        }
    }
