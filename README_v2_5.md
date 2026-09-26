# TAKWEEN v2.5 — Native IFC4 Export Foundation

v2.5 moves from an IFC-oriented intermediate model to a generated `.ifc` text file.

Implemented:
- IFC4 STEP header
- IfcProject
- IfcSite
- IfcBuilding
- IfcBuildingStorey
- IfcSpace
- spatial aggregation/containment relationships
- API endpoint `/projects/export-ifc`
- automated IFC output validation

Current limitation:
The writer is a foundation, not yet a full production BIM geometry exporter.
Native BRep/ExtrudedAreaSolid geometry, accurate placements, wall openings,
property sets, materials, and true IFC compressed GUID generation are next.
