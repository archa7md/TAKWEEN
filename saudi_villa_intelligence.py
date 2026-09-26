"""TAKWEEN v3.5 - Saudi Villa Design Intelligence."""
from copy import deepcopy
PUBLIC={"majlis","guest","guest_bath","reception","entrance","foyer","garage"}
FAMILY={"family_living","family","dining","bedroom","master_bedroom","bathroom","master_bath","dressing"}
SERVICE={"kitchen","service","maid","laundry","storage","mechanical"}

def rooms(a): return a.get("rooms",a.get("spaces",[])) or []
def name(r): return str(r.get("name",r.get("id",""))).lower().replace(" ","_").replace("-","_")
def kind(r):
 n=name(r)
 if "master" in n and "bed" in n:return "master_bedroom"
 if "bed" in n:return "bedroom"
 if "majlis" in n:return "majlis"
 if "family" in n and ("living" in n or n=="family"):return "family_living"
 if "kitchen" in n:return "kitchen"
 if "dining" in n:return "dining"
 if "entrance" in n or "foyer" in n:return "entrance"
 if "bath" in n:return "bathroom"
 if "dress" in n:return "dressing"
 if "laundry" in n:return "laundry"
 if "garage" in n or "parking" in n:return "garage"
 if "service" in n or "maid" in n:return "service"
 return n
def zone(r):
 k=kind(r)
 return "guest" if k in PUBLIC else "service" if k in SERVICE else "family" if k in FAMILY else "semi_private"
def center(r):
 x=float(r.get("x",r.get("x_m",0))); y=float(r.get("y",r.get("y_m",0)))
 w=float(r.get("w",r.get("width",r.get("width_m",0)))); h=float(r.get("h",r.get("depth",r.get("height",r.get("depth_m",0)))))
 return x+w/2,y+h/2
def dist(a,b):
 ax,ay=center(a); bx,by=center(b)
 return ((ax-bx)**2+(ay-by)**2)**0.5

def privacy_gradient(a):
 rs=rooms(a); score=0.; detail=[]
 gs=[r for r in rs if zone(r)=="guest"]; fs=[r for r in rs if zone(r)=="family"]
 for g in gs:
  for f in fs:
   d=dist(g,f); c=min(d/8,1)*.9; score+=c
   detail.append({"type":"guest_family_separation","guest":name(g),"family":name(f),"distance_m":round(d,2),"score":round(c,4)})
 entries=[r for r in rs if kind(r)=="entrance"]
 private=[r for r in rs if kind(r) in {"bedroom","master_bedroom","bathroom","master_bath","dressing"}]
 for e in entries:
  for p in private:
   d=dist(e,p)
   if d<4: score-=(4-d)*1.2
 return round(max(0,score),6),detail

def guest_family_separation(a):
 gs=[r for r in rooms(a) if zone(r)=="guest"]; fs=[r for r in rooms(a) if zone(r)=="family"]
 vals=[min(dist(g,f)/8,1) for g in gs for f in fs]
 return round(sum(vals)/max(len(vals),1),6)

def entrance_hierarchy(a):
 es=[r for r in rooms(a) if kind(r)=="entrance"]; targets=[r for r in rooms(a) if kind(r) in {"majlis","guest","guest_bath","foyer"}]
 score=sum(1/(1+dist(e,t)) for e in es for t in targets)
 return {"score":round(score,6)}

def outdoor_relationship(a):
 outdoor=[r for r in rooms(a) if str(r.get("type","")).lower() in {"courtyard","outdoor","garden","terrace"} or any(q in name(r) for q in ("courtyard","garden","terrace"))]
 targets=[r for r in rooms(a) if kind(r) in {"family_living","dining","majlis"}]
 score=sum(1/(1+dist(o,t)) for o in outdoor for t in targets)
 return {"score":round(score,6)}

def villa_metrics(a):
 p,_=privacy_gradient(a); eh=entrance_hierarchy(a); od=outdoor_relationship(a); gf=guest_family_separation(a)
 return {"saudi_villa_score":round(p+eh["score"]+od["score"]+gf,6),
 "privacy_gradient":p,"guest_family_separation":gf,"entrance_hierarchy":eh["score"],
 "outdoor_relationship":od["score"]}

def optimize_villa_intelligence(a):
 best=deepcopy(a)
 for r in rooms(best):
  if r.get("zone_locked"): continue
  r["design_zone"]=zone(r)
  r["privacy_level"]={"guest":"public_guest","family":"family_private","service":"service"}.get(r["design_zone"],"semi_private")
 m=villa_metrics(best)
 best["saudi_villa_v3_5"]={"engine":"saudi_villa_design_intelligence","score":m["saudi_villa_score"],
 "principles":["privacy_gradient","guest_family_separation","entrance_hierarchy","service_separation","family_outdoor_relationships"],
 "zone_summary":{name(r):r.get("design_zone") for r in rooms(best)}}
 return best,m
