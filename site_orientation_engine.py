"""TAKWEEN v3.6 - Site & Orientation Intelligence."""
from copy import deepcopy
def rooms(a): return a.get("rooms",a.get("spaces",[])) or []
def name(r): return str(r.get("name",r.get("id",""))).lower().replace(" ","_").replace("-","_")
def kind(r):
 n=name(r)
 if "master" in n and "bed" in n:return "master_bedroom"
 if "bed" in n:return "bedroom"
 if "majlis" in n:return "majlis"
 if "family" in n and "living" in n:return "family_living"
 if "kitchen" in n:return "kitchen"
 if "dining" in n:return "dining"
 if "entrance" in n or "foyer" in n:return "entrance"
 if "bath" in n:return "bathroom"
 if "garage" in n or "parking" in n:return "garage"
 return n
PREF={"master_bedroom":(.9,.9,.75),"bedroom":(.7,.85,.7),"family_living":(.85,.65,.85),"dining":(.7,.5,.75),"majlis":(.65,.55,.7),"kitchen":(.25,.4,.65),"bathroom":(.1,.9,.35),"entrance":(.15,.5,.4),"garage":(0,.2,.2)}
def site(a):
 s=a.get("site",{}) or {}; e=a.get("envelope",a.get("buildable_envelope",{})) or {}
 return {"width_m":float(s.get("width_m",e.get("width_m",e.get("width",10)))),"depth_m":float(s.get("depth_m",e.get("depth_m",e.get("depth",10)))),"north_deg":float(s.get("north_deg",a.get("north_deg",0))),"road_sides":s.get("road_sides",a.get("road_sides",["south"])),"view_sides":s.get("view_sides",a.get("view_sides",[])),"privacy_sides":s.get("privacy_sides",a.get("privacy_sides",[])),"setbacks":s.get("setbacks",a.get("setbacks",{})) or {}}
def side_score(a,r,side):
 s=site(a); p=PREF.get(kind(r),(.4,.5,.5)); side=side.lower(); score=(p[0] if side in [str(x).lower() for x in s["view_sides"]] else 0)+p[2]*.35
 if side in [str(x).lower() for x in s["road_sides"]]: score += 1.0 if kind(r)=="entrance" else (.55 if kind(r) in {"garage","majlis"} else -.65*p[1])
 if side in [str(x).lower() for x in s["privacy_sides"]]: score+=.55*p[1]
 return score
def setback_metrics(a):
 s=site(a); sb=s["setbacks"]; w=s["width_m"]; d=s["depth_m"]; l=float(sb.get("left",sb.get("west",0)) or 0); r=float(sb.get("right",sb.get("east",0)) or 0); f=float(sb.get("front",sb.get("south",0)) or 0); b=float(sb.get("rear",sb.get("north",0)) or 0)
 return {"site_width_m":w,"site_depth_m":d,"setbacks":{"left":l,"right":r,"front":f,"rear":b},"buildable_width_m":max(0,w-l-r),"buildable_depth_m":max(0,d-f-b)}
def orientation_metrics(a):
 total=0; rec=[]
 for r in rooms(a):
  vals={s:round(side_score(a,r,s),4) for s in ("north","east","south","west")}; best=max(vals,key=vals.get); total+=vals[best]; rec.append({"room":name(r),"kind":kind(r),"recommended_side":best,"scores":vals})
 return {"site":site(a),"setbacks":setback_metrics(a),"orientation_score":round(total,6),"room_recommendations":rec}
def optimize_site_orientation(a):
 best=deepcopy(a); m=orientation_metrics(best)
 for r in rooms(best):
  x=next(q for q in m["room_recommendations"] if q["room"]==name(r)); r["orientation_recommendation"]=x["recommended_side"]; r["orientation_scores"]=x["scores"]
 best["site_intelligence_v3_6"]={"engine":"site_orientation_intelligence","north_deg":site(best)["north_deg"],"orientation_score":m["orientation_score"],"buildable_width_m":m["setbacks"]["buildable_width_m"],"buildable_depth_m":m["setbacks"]["buildable_depth_m"],"recommendations":m["room_recommendations"]}
 return best,m
