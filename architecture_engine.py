def generate_project(brief,site):
 req=brief.get('requirements',{}); floors=int(req.get('floors',2)); beds=int(req.get('bedrooms',4)); al=[]
 for i,strategy in enumerate(['privacy-first','courtyard','linear','central-core','family-first','compact'],1):
  g=[{'id':f'F1-ENTRY-{i}','name':'Entrance / Foyer','area_m2':10,'geometry':{'x':0,'y':0,'w':3,'h':3.33}},{'id':f'F1-MAJLIS-{i}','name':'Majlis','area_m2':24,'geometry':{'x':3.2,'y':0,'w':4.8,'h':5}},{'id':f'F1-FAMILY-{i}','name':'Family Living','area_m2':28,'geometry':{'x':0,'y':5.3,'w':5.6,'h':5}}]
  u=[{'id':f'F2-BED-{i}-{b}','name':f'Bedroom {b}','area_m2':16,'geometry':{'x':((b-1)%2)*4.2,'y':((b-1)//2)*4.2,'w':3.8,'h':4}} for b in range(1,beds+1)]
  levels=[{'name':'Ground Floor','elevation_m':0,'rooms':g},{'name':'Upper Floor','elevation_m':3.3,'rooms':u}][:floors]
  al.append({'id':f'CONCEPT-{i}','strategy':strategy,'site_fit':{'width_m':site['derived']['buildable_width_m'],'depth_m':site['derived']['buildable_depth_m']},'parking':int(req.get('parking',2)),'levels':levels,'scores':{'adjacency':round(.75-i*.01,2),'privacy':round(.72+i*.01,2),'efficiency':.70}})
 return {'engine_version':'0.3-prototype','alternatives':al,'checks':{'overlap':'REVIEW','min_dimensions':'REVIEW','code':'REVIEW'},'limitations':['Rectangular starter geometry','No authoritative code verification','No IFC geometry writer yet']}
