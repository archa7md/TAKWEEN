
def generate_boq(project):
    items=[]
    for level in project.get("levels",[]):
        for room in level.get("rooms",[]):
            g=room.get("geometry",{}); w=float(g.get("w",0)); d=float(g.get("h",0))
            area=w*d; perimeter=2*(w+d)
            items += [
                {"category":"Floor Finish","description":room.get("name"),"unit":"m2","quantity":round(area,2)},
                {"category":"Ceiling","description":room.get("name"),"unit":"m2","quantity":round(area,2)},
                {"category":"Wall Paint","description":room.get("name"),"unit":"m2","quantity":round(perimeter*3.2,2)}
            ]
    elements = project.get("elements", [])
    if isinstance(elements, dict):
        flat=[]
        for group in elements.values():
            if isinstance(group, list): flat.extend(group)
        elements=flat
    for e in elements:
        if not isinstance(e, dict):
            continue
        entity=e.get("entity")
        g=e.get("geometry",{}) if isinstance(e.get("geometry"),dict) else {}
        if entity=="IfcWall":
            length=float(e.get("length_m", g.get("w",0) or g.get("width_m",0)))
            height=float(e.get("height_m",3.2))
            items.append({"category":"Wall","description":e.get("material","Wall"),
                          "unit":"m2","quantity":round(length*height,2)})
        elif entity=="IfcDoor":
            items.append({"category":"Door","description":e.get("material","Door"),
                          "unit":"item","quantity":1})
        elif entity=="IfcWindow":
            items.append({"category":"Window","description":e.get("material","Window"),
                          "unit":"item","quantity":1})
        elif entity=="IfcSlab":
            area=float(e.get("area_m2", g.get("area_m2",0)))
            items.append({"category":"Slab","description":e.get("level"),
                          "unit":"m2","quantity":round(area,2)})
    return {"boq_version":"0.2","status":"PRELIMINARY","basis":"Architectural BIM + materials","items":items}
