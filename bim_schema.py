SCHEMA_ID='TAKWEEN-BIM-INTERMEDIATE-1.3'
def build_bim_model(project):
 spaces=[]
 for level in project.get('levels',[]):
  for r in level.get('rooms',[]): spaces.append({'entity':'IfcSpace','id':r.get('id'),'name':r.get('name'),'level':level.get('name'),'area_m2':r.get('area_m2'),'geometry':r.get('geometry',{})})
 if not spaces:
  for a in project.get('alternatives',[]):
   for level in a.get('levels',[]):
    for r in level.get('rooms',[]): spaces.append({'entity':'IfcSpace','id':r.get('id'),'name':r.get('name'),'level':level.get('name'),'area_m2':r.get('area_m2'),'geometry':r.get('geometry',{})})
 return {'schema_id':SCHEMA_ID,'project_id':project.get('project_id','TAKWEEN-PROJECT'),'export_targets':['IFC4','REVIT'],'status':'INTERMEDIATE_MODEL','spaces':spaces,'future_entities':['IfcWall','IfcDoor','IfcWindow','IfcStair','IfcSlab']}


def build_physical_model(project: dict) -> dict:
    from .ifc_bridge import build_ifc_intermediate
    return build_ifc_intermediate(project)
