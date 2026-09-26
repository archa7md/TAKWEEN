"""TAKWEEN v3.4 Multi-Floor Intelligent Planning."""
from copy import deepcopy

PUBLIC={"entrance","foyer","majlis","guest","guest_bath","dining","garage"}
PRIVATE={"master_bedroom","bedroom","master_bath","bathroom","dressing","family","family_living"}
SERVICE={"kitchen","laundry","service","maid","storage","mechanical"}

PREFERRED={
 "entrance":0,"majlis":0,"guest":0,"guest_bath":0,"garage":0,
 "kitchen":0,"dining":0,"family_living":0,"family":1,
 "master_bedroom":1,"bedroom":1,"master_bath":1,"bathroom":1,
 "dressing":1,"laundry":1,"service":1,"maid":1,"storage":0
}

def rooms(a): return a.get("rooms",a.get("spaces",[])) or []
def name(r): return str(r.get("name",r.get("id",""))).lower().replace(" ","_").replace("-","_")
def kind(r):
 n=name(r)
 if "master" in n and "bed" in n: return "master_bedroom"
 if "bed" in n: return "bedroom"
 if "majlis" in n: return "majlis"
 if "family" in n and ("living" in n or n=="family"): return "family_living"
 if "kitchen" in n: return "kitchen"
 if "dining" in n: return "dining"
 if "entrance" in n or "foyer" in n: return "entrance"
 if "bath" in n: return "bathroom"
 if "dress" in n: return "dressing"
 if "laundry" in n: return "laundry"
 if "garage" in n or "parking" in n: return "garage"
 if "service" in n or "maid" in n: return "service"
 return n
def zone(r):
 k=kind(r)
 return "public" if k in PUBLIC else "private" if k in PRIVATE else "service" if k in SERVICE else "semi_private"
def preferred_floor(r): return PREFERRED.get(kind(r),0)

def vertical_demand(a):
 details=[]; demand=0
 for r in rooms(a):
  f=int(r.get("floor",r.get("level",0)) or 0); p=preferred_floor(r)
  if f!=p:
   q=1+abs(f-p)*.5; demand+=q
   details.append({"room":name(r),"assigned_floor":f,"preferred_floor":p,"penalty":round(q,3)})
  if f>0 and zone(r)=="public":
   demand+=1.25; details.append({"room":name(r),"type":"public_upstairs","penalty":1.25})
  if f==0 and zone(r)=="private":
   demand+=.75; details.append({"room":name(r),"type":"private_ground","penalty":.75})
 return {"vertical_demand":round(demand,6),"details":details,
         "floor_count":int(a.get("floors",a.get("floor_count",2)) or 2)}

def floor_distribution(a):
 out={}
 for r in rooms(a):
  f=str(int(r.get("floor",r.get("level",0)) or 0))
  out.setdefault(f,[]).append(name(r))
 return out

def connectivity_score(a):
 score=0; details=[]
 for r in rooms(a):
  f=int(r.get("floor",r.get("level",0)) or 0); k=kind(r)
  if f>0 and k in {"bedroom","master_bedroom","family_living","bathroom","master_bath"}:
   score+=1; details.append({"room":name(r),"reason":"private_upper","score":1})
  if f==0 and k in {"entrance","majlis","garage","kitchen","dining"}:
   score+=1; details.append({"room":name(r),"reason":"ground_public_service","score":1})
 return {"connectivity_score":score,"details":details}

def choose_stair_position(a):
 env=a.get("envelope",a.get("buildable_envelope",{})) or {}
 w=float(env.get("width_m",env.get("width",10)) or 10)
 d=float(env.get("depth_m",env.get("depth",10)) or 10)
 p=a.get("stair_position")
 if isinstance(p,dict) and "x" in p and "y" in p:
  return {"x":float(p["x"]),"y":float(p["y"]),
          "width_m":float(p.get("width_m",1.2)),"depth_m":float(p.get("depth_m",4))}
 return {"x":round(max(0,w/2-.75),3),"y":round(max(0,d-4.5),3),
         "width_m":1.5,"depth_m":4.0}

def optimize_floors(a):
 best=deepcopy(a)
 before=vertical_demand(best)["vertical_demand"]
 max_floor=max(0,int(best.get("floors",best.get("floor_count",2)) or 2)-1)
 for r in rooms(best):
  if r.get("floor_locked") or r.get("level_locked"): continue
  f=min(preferred_floor(r),max_floor)
  r["floor"]=f; r["level"]=f
 best["stair"]=choose_stair_position(best)
 after=vertical_demand(best)["vertical_demand"]
 best["multi_floor_v3_4"]={
  "engine":"multi_floor_intelligent_planning",
  "before_vertical_demand":round(before,6),
  "after_vertical_demand":round(after,6),
  "demand_reduction":round(before-after,6),
  "floor_distribution":floor_distribution(best),
  "connectivity":connectivity_score(best),
  "stair":best["stair"]}
 return best

def plan_multi_floor(a):
 s=optimize_floors(a)
 return {"alternative":s,"vertical_analysis":vertical_demand(s),
         "floor_distribution":floor_distribution(s),
         "connectivity":connectivity_score(s),"stair":s["stair"]}
