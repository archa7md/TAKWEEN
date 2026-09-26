# TAKWEEN v2.4 — IFC/Revit Bridge Foundation

Adds a physical BIM element layer on top of v2.3:
- IfcWall
- IfcDoor
- IfcWindow
- IfcSlab
- IfcStair
- IFC4-oriented intermediate schema
- API endpoint: `/projects/ifc-intermediate`
- Automated v2.4 regression test

Important: this is NOT yet a native `.ifc` file writer and does not create a `.rvt` file.
The next milestone is a real IFC4 writer with placements, local coordinate systems,
property sets and relationships, followed by a Revit bridge.
