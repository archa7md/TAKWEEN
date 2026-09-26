from copy import deepcopy
DEFAULT_WEIGHTS={"geometry":.22,"adjacency":.18,"privacy":.16,"efficiency":.12,"orientation":.12,"multi_floor":.10,"site":.10}
def _n(x,d=0):
 try:return float(x)
 except:return d
def score_alternative(a,weights=None):
 w=dict(DEFAULT_WEIGHTS); w.update(weights or {})
 try:
  from backend.geometry_metrics import metrics as gm; g=gm(a)
 except Exception:g={}
 try:
  from saudi_villa_intelligence import villa_metrics; v=villa_metrics(a)
 except Exception:v={}
 try:
  from site_orientation_engine import orientation_metrics; o=orientation_metrics(a)
 except Exception:o={}
 try:
  from multi_floor_engine import vertical_demand; f=vertical_demand(a)
 except Exception:f={"vertical_demand":0}
 ge=max(0,min(1,_n(g.get("area_efficiency",g.get("envelope_fit",0)))))
 privacy=max(0,min(1,_n(v.get("privacy_gradient",0))/5)); adj=max(0,min(1,_n(v.get("guest_family_separation",0))))
 ori=max(0,min(1,_n(o.get("orientation_score",0))/(max(1,len(o.get("room_recommendations",[])))*1.5))); floor=1/(1+max(0,_n(f.get("vertical_demand",0))))
 c={"geometry":ge,"adjacency":adj,"privacy":privacy,"efficiency":ge,"orientation":ori,"multi_floor":floor,"site":ori}
 return {"score":round(sum(c[k]*w[k] for k in c),6),"weights":w,"components":{k:round(x,6) for k,x in c.items()},"geometry_metrics":g,"villa_metrics":v,"orientation_metrics":o,"vertical_metrics":f}
def rank_alternatives(alternatives,weights=None,top_k=6):
 rows=[]
 for i,a in enumerate(alternatives):
  r=score_alternative(a,weights); item=deepcopy(a); order=sorted(r["components"].items(),key=lambda x:x[1],reverse=True)
  item["unified_design_intelligence_v3_7"]={"alternative_index":i,"score":r["score"],"components":r["components"],"weights":r["weights"],"decision_summary":{"strongest_factors":[x[0] for x in order[:3]],"weakest_factors":[x[0] for x in order[-2:]]}}; rows.append((r["score"],item))
 rows.sort(key=lambda x:x[0],reverse=True)
 for rank,(_,item) in enumerate(rows[:top_k],1): item["unified_design_intelligence_v3_7"]["rank"]=rank
 return [x[1] for x in rows[:top_k]]
def unified_project_analysis(project,weights=None,top_k=6):
 alts=project.get("alternatives"); alts=alts if isinstance(alts,list) else [project]
 return {"engine":"TAKWEEN Unified Design Intelligence","version":"3.7","alternatives_count":len(alts),"ranked_alternatives":rank_alternatives(alts,weights,top_k),"weights":dict(DEFAULT_WEIGHTS,**(weights or {})),"note":"Explainable design-assistance score; not code-compliance verdict."}
