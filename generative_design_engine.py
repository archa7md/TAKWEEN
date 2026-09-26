"""TAKWEEN v4.0 - Generative Design Engine.

Generates deterministic architectural alternatives from an existing parametric
alternative/brief, then scores them with the v3.7 intelligence stack and can
optionally pass the strongest candidates through the v3.9 iteration layer.
This is bounded parametric generation, not an autonomous final-design system.
"""
from __future__ import annotations
from copy import deepcopy
from math import hypot
from unified_design_engine import score_alternative, DEFAULT_WEIGHTS


def _rooms(a):
    if isinstance(a.get("levels"), list):
        out=[]
        for li,lvl in enumerate(a["levels"]):
            for ri,r in enumerate(lvl.get("rooms", [])):
                out.append((r,li,ri))
        return out
    rs=a.get("rooms") or a.get("spaces") or []
    return [(r,None,i) for i,r in enumerate(rs)]


def _geom(r):
    g=r.get("geometry") if isinstance(r.get("geometry"),dict) else r
    return g,float(g.get("x",g.get("x_m",0))),float(g.get("y",g.get("y_m",0))),float(g.get("w",g.get("width_m",g.get("width",0)))),float(g.get("h",g.get("depth_m",g.get("depth",0))))


def _setxy(r,x,y):
    g=r.get("geometry") if isinstance(r.get("geometry"),dict) else r
    if "x_m" in g and "x" not in g: g["x_m"]=round(x,3)
    else: g["x"]=round(x,3)
    if "y_m" in g and "y" not in g: g["y_m"]=round(y,3)
    else: g["y"]=round(y,3)


def _bounds(a):
    for key in ("site_fit","buildable_envelope","envelope","site"):
        e=a.get(key)
        if isinstance(e,dict):
            w=e.get("width_m",e.get("width")); h=e.get("depth_m",e.get("depth"))
            if w is not None and h is not None:return float(w),float(h)
    return None


def _clamp(a):
    b=_bounds(a)
    if not b:return
    W,H=b
    for r,_,_ in _rooms(a):
        _,x,y,w,h=_geom(r)
        _setxy(r,max(0,min(x,W-w)),max(0,min(y,H-h)))


def _translate(a,dx,dy):
    c=deepcopy(a)
    for r,_,_ in _rooms(c):
        _,x,y,_,_=_geom(r); _setxy(r,x+dx,y+dy)
    _clamp(c); return c


def _mirror_x(a):
    c=deepcopy(a); b=_bounds(c)
    if not b:return c
    W,_=b
    for r,_,_ in _rooms(c):
        _,x,y,w,_=_geom(r); _setxy(r,W-x-w,y)
    return c


def _mirror_y(a):
    c=deepcopy(a); b=_bounds(c)
    if not b:return c
    _,H=b
    for r,_,_ in _rooms(c):
        _,x,y,_,h=_geom(r); _setxy(r,x,H-y-h)
    return c


def _compact(a,factor=0.94):
    c=deepcopy(a)
    rs=_rooms(c)
    if not rs:return c
    cx=sum(_geom(r)[1]+_geom(r)[3]/2 for r,_,_ in rs)/len(rs)
    cy=sum(_geom(r)[2]+_geom(r)[4]/2 for r,_,_ in rs)/len(rs)
    for r,_,_ in rs:
        _,x,y,_,_=_geom(r); _setxy(r,cx+(x-cx)*factor,cy+(y-cy)*factor)
    _clamp(c); return c


def _zone_shift(a,public_to_front=True):
    c=deepcopy(a)
    rs=_rooms(c)
    b=_bounds(c)
    if not b:return c
    W,H=b
    public_words=("majlis","guest","reception","foyer","entrance")
    private_words=("master","bed","family","private")
    for r,_,_ in rs:
        n=str(r.get("name",r.get("id",""))).lower(); _,x,y,w,h=_geom(r)
        if any(q in n for q in public_words):
            _setxy(r,x, max(0, y-1.2) if public_to_front else min(H-h,y+1.2))
        elif any(q in n for q in private_words):
            _setxy(r,x, min(H-h,y+1.2) if public_to_front else max(0,y-1.2))
    _clamp(c); return c


def _dedupe(candidates):
    out=[]; seen=set()
    for label,a in candidates:
        sig=[]
        for r,li,ri in _rooms(a):
            _,x,y,w,h=_geom(r); sig.append((li,ri,round(x,2),round(y,2),round(w,2),round(h,2)))
        key=tuple(sig)
        if key not in seen:seen.add(key);out.append((label,a))
    return out


def generate_alternatives(base, count=8, strategy="balanced"):
    count=max(1,min(int(count),12))
    candidates=[("baseline",deepcopy(base)),
                ("mirror_x",_mirror_x(base)),
                ("mirror_y",_mirror_y(base)),
                ("compact",_compact(base,.92)),
                ("expanded",_compact(base,1.06)),
                ("public_front",_zone_shift(base,True)),
                ("private_back",_zone_shift(base,False)),
                ("shift_right",_translate(base,1.0,0)),
                ("shift_back",_translate(base,0,1.0))]
    candidates=_dedupe(candidates)
    return [{"generation_strategy":label, "alternative":a} for label,a in candidates[:count]]


def generate_project(project, weights=None, count=8, refine=True):
    base_alts=project.get("alternatives") if isinstance(project,dict) else None
    if isinstance(base_alts,list) and base_alts: base=base_alts[0]
    elif isinstance(project,dict) and "alternative" in project: base=project["alternative"]
    else: base=project
    generated=generate_alternatives(base,count)
    scored=[]
    for row in generated:
        s=score_alternative(row["alternative"],weights)
        item=deepcopy(row["alternative"])
        item["generative_design_v4_0"]={"strategy":row["generation_strategy"],"score":s["score"],"components":s["components"],"weights":s["weights"]}
        scored.append((s["score"],row["generation_strategy"],item,s))
    scored.sort(key=lambda x:x[0],reverse=True)
    results=[]
    for rank,(score,label,item,s) in enumerate(scored,1):
        entry={"rank":rank,"strategy":label,"score":score,"components":s["components"],"alternative":item}
        if refine:
            try:
                from design_iteration_engine import iterate_alternative
                it=iterate_alternative(item,weights=weights)
                entry["iteration"]={"status":it["status"],"score_delta":it["score_delta"],"selected_factor":it["selected_factor"]}
                if it["status"]=="improved":
                    entry["refined_alternative"]=it["alternative"]
                    entry["refined_score"]=it["after"]["score"]
            except Exception as exc:
                entry["iteration"]={"status":"skipped","reason":str(exc)}
        results.append(entry)
    return {"engine":"TAKWEEN Generative Design Engine","version":"4.0","generated_count":len(results),"requested_count":count,"results":results,"weights":dict(DEFAULT_WEIGHTS,**(weights or {})),"trace":{"generation":"deterministic bounded geometric transformations","refinement":"v3.9 Design Iteration Engine"},"limitations":["Generation is parametric and deterministic; it is not an LLM or global generative optimizer.","Geometry remains simplified rectangular prototype geometry.","Orientation is heuristic and not a solar simulation.","No Saudi code or municipality compliance is inferred.","Architect review is required before design use."]}
