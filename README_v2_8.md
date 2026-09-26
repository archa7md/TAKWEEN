# TAKWEEN v2.8 — Wall & Opening Engine

Adds:
- Segmented architectural wall model.
- External/internal wall classification.
- 250 mm external wall and 200 mm internal wall types.
- Individual wall segments with axis, length, thickness and height.
- Door elements with size, swing and placement.
- Window elements with size, sill height and placement.
- Material/type metadata.
- BOQ quantities tied to segmented walls/openings.
- API endpoint `/projects/wall-openings`.

Next: v2.9 should build true wall-opening subtraction and IFC geometry
relationships so doors/windows become actual voids hosted in wall geometry.
