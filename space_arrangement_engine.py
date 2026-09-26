"""TAKWEEN v3.3 - Intelligent Space Arrangement."""
from copy import deepcopy
import math

PUBLIC={"entrance","foyer","majlis","guest","guest_bath","dining","garage"}
PRIVATE={"master_bedroom","bedroom","master_bath","bathroom","dressing","family","family_living"}
SERVICE={"kitchen","laundry","service","maid","storage","mechanical"}

REL={
 "entrance":{"majlis":1.0,"foyer":1.0,"guest_bath":.9},
 "majlis":{"entrance":1.0,"guest_bath":.8},
 "family_living":{"dining":.9,"kitchen":.85},
 "kitchen":{"dining":.9,"service":.85,"family_living":.75},
 "bedroom":{"family_living":.55,"bathroom":.8},
 "master_bedroom":{"master_bath":.95,"dressing":.9},
 "laundry":{"kitchen":.7,"service":.8},
 "garage":{"entrance":.8,"service":.65},
}
SEP={tuple(sorted(x)):v for x,v in {
 ("majlis","master_bedroom"):1.0,
 ("majlis","bedroom"):.85,
 ("majlis","family_living"):.55,
}.items()}

def rooms(a): return a.get("rooms",a.get("spaces",[])) or []
def name(r): return str(r.get("name",r.get("id",""))).lower().replace(" ","_").replace("-","_")
def kind(r):
 n=name(r)
 if "master" in n and ("bed" in n or n=="master"): return "master_bedroom"
 if "bed" in n: return "bedroom"
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
def xywh(r):
 return (float(r.get("x",r.get("x_m",0))),float(r.get("y",r.get("y_m",0))),
         float(r.get("w",r.get("width",r.get("width_m",0)))),
         float(r.get("h",r.get("depth",r.get("height",r.get("depth_m",0))))))
def center(r):
 x,y,w,h=xywh(r); return x+w/2,y+h/2
def dist(a,b):
 ax,ay=center(a); bx,by=center(b); return math.hypot(ax-bx,ay-by)
def zone(r):
 k=kind(r)
 return "public" if k in PUBLIC else "private" if k in PRIVATE else "service" if k in SERVICE else "semi_private"

def arrangement_metrics(a):
 rs=rooms(a); score=0.; detail=[]
 for i,x in enumerate(rs):
  kx=kind(x)
  for y in rs[i+1:]:
   ky=kind(y); d=dist(x,y)
   w=REL.get(kx,{}).get(ky,REL.get(ky,{}).get(kx,0))
   if w:
    c=w/(1+d); score+=c
    detail.append({"a":name(x),"b":name(y),"type":"adjacency","weight":w,"distance_m":round(d,3),"contribution":round(c,4)})
   s=SEP.get(tuple(sorted((kx,ky))),0)
   if s:
    c=s*min(d/10,1); score+=c
    detail.append({"a":name(x),"b":name(y),"type":"separation","weight":s,"distance_m":round(d,3),"contribution":round(c,4)})
 penalty=0.
 for x in rs:
  for y in rs:
   if x is y: continue
   if zone(x)=="public" and zone(y)=="private" and dist(x,y)<2.5:
    penalty+=(2.5-dist(x,y))*.5
 return {"relationship_score":round(score,6),"public_private_penalty":round(penalty,6),
         "arrangement_score":round(score-penalty,6),"relationships":detail}

def optimize_arrangement(a,iterations=80,step_m=.5):
 best=deepcopy(a); before=arrangement_metrics(best)["arrangement_score"]; bestscore=before
 rs=rooms(best)
 for _ in range(iterations):
  improved=False
  for i,r in enumerate(list(rs)):
   x,y,w,h=xywh(r)
   for dx,dy in ((step_m,0),(-step_m,0),(0,step_m),(0,-step_m)):
    t=deepcopy(best); tr=rooms(t)[i]; nx,ny=x+dx,y+dy
    env=t.get("envelope",t.get("buildable_envelope"))
    if isinstance(env,dict):
     W=env.get("width_m",env.get("width")); H=env.get("depth_m",env.get("depth"))
     if W is not None and H is not None and (nx<0 or ny<0 or nx+w>float(W) or ny+h>float(H)): continue
    tr["x"]=round(nx,3); tr["y"]=round(ny,3)
    s=arrangement_metrics(t)["arrangement_score"]
    if s>bestscore+1e-9: best,bestscore=t,s; improved=True
  if not improved: break
 m=arrangement_metrics(best)
 best["arrangement_v3_3"]={"engine":"intelligent_space_arrangement",
  "method":"deterministic_relationship_local_search","before_score":round(before,6),
  "after_score":round(m["arrangement_score"],6),"score_delta":round(m["arrangement_score"]-before,6),
  "zones":{str(r.get("name",r.get("id","room"))):zone(r) for r in rooms(best)}}
 return best,m
