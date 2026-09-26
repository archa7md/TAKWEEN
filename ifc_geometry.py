def add_geometry(project):
    for level in project.get("levels", []):
        for room in level.get("rooms", []):
            g=room.get("geometry", {})
            room["geometry_3d"]={"type":"IfcExtrudedAreaSolid","profile":"Rectangle",
                "width_m":float(g.get("w",3)),"depth_m":float(g.get("h",3)),"height_m":3.0,
                "placement":{"x_m":float(g.get("x",0)),"y_m":float(g.get("y",0)),
                             "z_m":float(level.get("elevation_m",0))}}
    return project
