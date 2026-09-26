# TAKWEEN v2.9 — Openings + Materials + BOQ

Adds:
- IfcOpeningElement representation.
- IfcRelVoidsElement relationship from wall to opening.
- IfcRelFillsElement relationship from opening to door/window.
- Material metadata for walls, doors, windows and slabs.
- Floor, ceiling and wall-paint finish quantities.
- BOQ v0.2 linked to architectural BIM elements.
- APIs: `/projects/openings`, `/projects/materials`.

This is still an intermediate BIM model. Native IFC geometric subtraction,
exact wall topology, and production Revit synchronization remain future work.
