
import uuid
from pathlib import Path
from typing import Dict, Any

def guid():
    # IFC compressed GUID is not implemented here; deterministic 22-char ASCII token is used
    return uuid.uuid4().hex[:22]

def esc(s):
    return str(s).replace("'", "''")

class IFCWriter:
    def __init__(self):
        self.lines = []
        self.i = 1
        self.refs = {}

    def add(self, entity, *args):
        n = self.i
        self.i += 1
        self.lines.append(f"#{n}={entity}({','.join(args)});")
        return n

    def write(self, project: Dict[str, Any], path: str):
        # Accept either a selected concept or the full engine response.
        if not project.get('levels') and project.get('alternatives'):
            project = project['alternatives'][0]
        self.lines = []
        self.i = 1

        self.lines += [
            "ISO-10303-21;",
            "HEADER;",
            "FILE_DESCRIPTION(('ViewDefinition [CoordinationView_V2.0]'),'2;1');",
            "FILE_NAME('TAKWEEN_generated.ifc','2026-09-20T00:00:00',('TAKWEEN'),('TAKWEEN'),'TAKWEEN IFC Writer','TAKWEEN','');",
            "FILE_SCHEMA(('IFC4'));",
            "ENDSEC;",
            "DATA;"
        ]

        owner = self.add("IFCPERSONANDORGANIZATION",
                         "$,$,$,$,$,$,$")
        app = self.add("IFCAPPLICATION", f"#{owner}", "'TAKWEEN'", "'TAKWEEN IFC Writer'", "'TAKWEEN'")
        history = self.add("IFCOWNERHISTORY", f"#{owner}", f"#{app}", "$","$","$","$","$","$","$")
        project_id = self.add("IFCPROJECT", f"'{guid()}'", f"#{history}", "'TAKWEEN Project'", "$", "$", "$", "$", "$")
        context = self.add("IFCGEOMETRICREPRESENTATIONCONTEXT", "'Model'", "'Model'", "3", "1.0E-5", "$", "$")

        site_id = self.add("IFCSITE", f"'{guid()}'", f"#{history}", "'TAKWEEN Site'", "$","$","$","$","$","$","$","$","$","$","$")
        building_id = self.add("IFCBUILDING", f"'{guid()}'", f"#{history}", "'TAKWEEN Villa'", "$","$","$","$","$","$","$","$","$","$","$")
        project["ifc_ids"] = {"project": project_id, "site": site_id, "building": building_id}

        storeys = []
        for level in project.get("levels", []):
            storeys.append(self.add(
                "IFCBUILDINGSTOREY", f"'{guid()}'", f"#{history}",
                f"'{esc(level.get('name','Level'))}'", "$","$","$",
                f"{float(level.get('elevation_m',0)):.3f}", "$"
            ))

        # Spatial containment relations
        self.add("IFCRELAGGREGATES", f"'{guid()}'", f"#{history}", "$","$",
                 f"#{project_id}", "(" + ",".join(f"#{x}" for x in [site_id]) + ")")
        self.add("IFCRELAGGREGATES", f"'{guid()}'", f"#{history}", "$","$",
                 f"#{site_id}", f"(#{building_id})")
        self.add("IFCRELAGGREGATES", f"'{guid()}'", f"#{history}", "$","$",
                 f"#{building_id}", "(" + ",".join(f"#{x}" for x in storeys) + ")")

        for li, level in enumerate(project.get("levels", [])):
            sid = storeys[li]
            for room in level.get("rooms", []):
                rid = self.add(
                    "IFCSPACE", f"'{guid()}'", f"#{history}",
                    f"'{esc(room.get('name','Space'))}'", "$","$","$","$","$",
                    f"'{esc(room.get('id','SPACE'))}'", "$"
                )
                self.add("IFCRELCONTAINEDINSPATIALSTRUCTURE",
                         f"'{guid()}'", f"#{history}", "$","$",
                         f"(#{rid})", f"#{sid}")

        out = Path(path)
        out.write_text("\n".join(self.lines) + "\nENDSEC;\nEND-ISO-10303-21;\n", encoding="utf-8")
        return str(out)

def export_ifc(project: Dict[str, Any], path: str):
    return IFCWriter().write(project, path)
