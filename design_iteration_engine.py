"""TAKWEEN v3.9 - Design Iteration Engine.

Turns v3.8 explainable recommendations into deterministic candidate edits,
re-scores the edited alternatives, and reports before/after impact. This is a
bounded design-assistance layer, not a global optimizer or code checker.
"""
from __future__ import annotations
from copy import deepcopy
from math import hypot
from unified_design_engine import score_alternative, DEFAULT_WEIGHTS

PRIVATE_WORDS = ("bed", "master", "private", "family")
PUBLIC_WORDS = ("majlis", "entrance", "foyer", "guest", "reception")
KITCHEN_WORDS = ("kitchen",)
DINING_WORDS = ("dining", "dining room")


def _rooms(a):
    if isinstance(a.get("levels"), list):
        out=[]
        for li, level in enumerate(a["levels"]):
            for ri, room in enumerate(level.get("rooms", [])):
                out.append((room, li, ri))
        return out
    rooms=a.get("rooms") or a.get("spaces") or []
    return [(r, None, i) for i,r in enumerate(rooms)]


def _name(r): return str(r.get("name", r.get("id", "room"))).lower()

def _geom(r):
    g=r.get("geometry") if isinstance(r.get("geometry"),dict) else r
    return g, float(g.get("x",g.get("x_m",0))), float(g.get("y",g.get("y_m",0))), float(g.get("w",g.get("width_m",g.get("width",0)))), float(g.get("h",g.get("depth_m",g.get("depth",0))))


def _setxy(r,x,y):
    target=r.get("geometry") if isinstance(r.get("geometry"),dict) else r
    if "x" in target or "x_m" not in target: target["x"]=round(x,3)
    else: target["x_m"]=round(x,3)
    if "y" in target or "y_m" not in target: target["y"]=round(y,3)
    else: target["y_m"]=round(y,3)


def _bounds(a):
    for key in ("site_fit","buildable_envelope","envelope","site"):
        e=a.get(key)
        if isinstance(e,dict):
            w=e.get("width_m",e.get("width")); h=e.get("depth_m",e.get("depth"))
            if w is not None and h is not None: return float(w),float(h)
    return None


def _valid(a):
    bounds=_bounds(a); rs=[r for r,_,_ in _rooms(a)]
    violations=[]
    if bounds:
        W,H=bounds
        for r in rs:
            _,x,y,w,h=_geom(r)
            if x < 0 or y < 0 or x+w > W or y+h > H: violations.append(("envelope",r.get("name")))
    for i,a1 in enumerate(rs):
        _,x1,y1,w1,h1=_geom(a1)
        for b1 in rs[i+1:]:
            _,x2,y2,w2,h2=_geom(b1)
            ix=max(0,min(x1+w1,x2+w2)-max(x1,x2)); iy=max(0,min(y1+h1,y2+h2)-max(y1,y2))
            if ix*iy > 0.04: violations.append(("overlap",a1.get("name"),b1.get("name")))
    return violations


def _centroid(rs):
    pts=[]
    for r in rs:
        _,x,y,w,h=_geom(r); pts.append((x+w/2,y+h/2))
    if not pts:return (0,0)
    return (sum(x for x,_ in pts)/len(pts),sum(y for _,y in pts)/len(pts))


def _move_toward(a, source, target, step=1.0):
    _,sx,sy,_,_=_geom(source); _,tx,ty,_,_=_geom(target)
    cx=sx; cy=sy
    dx=tx-cx; dy=ty-cy; d=hypot(dx,dy)
    if d < 1e-9:return
    _setxy(source,cx+dx/d*step,cy+dy/d*step)


def _candidate_edits(alternative, weak_factors):
    base=deepcopy(alternative); candidates=[]
    rs=[r for r,_,_ in _rooms(base)]
    names=[(_name(r),r) for r in rs]
    public=[r for n,r in names if any(w in n for w in PUBLIC_WORDS)]
    private=[r for n,r in names if any(w in n for w in PRIVATE_WORDS)]
    kitchen=[r for n,r in names if any(w in n for w in KITCHEN_WORDS)]
    dining=[r for n,r in names if any(w in n for w in DINING_WORDS)]

    for factor in weak_factors:
        c=deepcopy(alternative); cr=[r for r,_,_ in _rooms(c)]
        if factor == "privacy" and private and public:
            ppub=_centroid([r for n,r in [(_name(r),r) for r in cr] if any(w in n for w in PUBLIC_WORDS)])
            ppriv=_centroid([r for n,r in [(_name(r),r) for r in cr] if any(w in n for w in PRIVATE_WORDS)])
            # Move private rooms one metre farther from the public centroid.
            for n,r in [(_name(r),r) for r in cr]:
                if any(w in n for w in PRIVATE_WORDS):
                    _,x,y,_,_=_geom(r); dx=x-ppub[0]; dy=y-ppub[1]; d=hypot(dx,dy) or 1
                    _setxy(r,x+dx/d,y+dy/d)
        elif factor == "adjacency" and kitchen and dining:
            # Move kitchen toward the first dining space.
            _move_toward(c,kitchen[0],dining[0],1.0)
        elif factor in ("orientation","site") and private:
            # For north-oriented prototypes, move private rooms toward the
            # higher-y side. This remains a heuristic and is explicitly traced.
            for r in private:
                _,x,y,_,_= _geom(r); _setxy(r,x,y+1.0)
        elif factor == "geometry":
            bounds=_bounds(c)
            if bounds:
                W,H=bounds
                for r in cr:
                    _,x,y,w,h=_geom(r); _setxy(r,max(0,min(x,W-w)),max(0,min(y,H-h)))
        elif factor == "efficiency" and public:
            # Reduce unnecessary separation by moving the entrance/foyer
            # toward the public centroid without changing room dimensions.
            target=_centroid(public)
            for r in public[:1]: _move_toward(c,r,{"geometry":{"x":target[0],"y":target[1],"w":0,"h":0}},0.5)
        elif factor == "multi_floor":
            # No room reassignment is fabricated here; annotate as review-only.
            pass
        else:
            continue
        candidates.append((factor,c))
    return candidates


def iterate_alternative(alternative, decision=None, weights=None, min_improvement=0.0001):
    weights=dict(DEFAULT_WEIGHTS,**(weights or {}))
    before=score_alternative(alternative,weights)
    weak=[]
    if isinstance(decision,dict):
        weak=[x.get("factor") for x in decision.get("factor_trace",[]) if x.get("score",1)>=0 and x.get("score",1)<0.55]
    if not weak:
        weak=[k for k,v in before["components"].items() if v<0.55]
    candidates=_candidate_edits(alternative,[x for x in weak if x])
    evaluated=[]
    for factor,c in candidates:
        violations=_valid(c)
        scored=score_alternative(c,weights)
        evaluated.append({"factor":factor,"alternative":c,"score":scored["score"],"score_delta":round(scored["score"]-before["score"],6),"violations":violations,"components":scored["components"]})
    feasible=[x for x in evaluated if not x["violations"]]
    improving=[x for x in feasible if x["score"]>before["score"]+min_improvement]
    best=max(improving or feasible or evaluated, key=lambda x:x["score"]) if (improving or feasible or evaluated) else None
    if best and best["score"]>before["score"]+min_improvement:
        status="improved"
        selected=best
    else:
        status="no_improvement"
        selected=None
    after=score_alternative(selected["alternative"],weights) if selected else before
    return {
        "engine":"TAKWEEN Design Iteration Engine","version":"3.9","status":status,
        "before":{"score":before["score"],"components":before["components"]},
        "after":{"score":after["score"],"components":after["components"]},
        "score_delta":round(after["score"]-before["score"],6),
        "selected_factor":selected["factor"] if selected else None,
        "alternative":selected["alternative"] if selected else deepcopy(alternative),
        "candidate_count":len(evaluated),
        "candidates":[{k:v for k,v in x.items() if k!="alternative"} for x in evaluated],
        "constraint_status":"PASS" if not _valid(after_alt := (selected["alternative"] if selected else alternative)) else "REVIEW",
        "trace":{"weak_factors":weak,"weights":weights,"min_improvement":min_improvement},
        "limitations":["Bounded deterministic edits; not a global optimizer.","Orientation edits are heuristic and are not solar simulation.","No Saudi code or municipality compliance is inferred.","Architect review remains required."],
    }


def iterate_project(project, weights=None, top_k=6):
    alts=project.get("alternatives") if isinstance(project,dict) else None
    if not isinstance(alts,list): alts=[project]
    decisions=project.get("decisions") if isinstance(project,dict) else None
    results=[]
    for i,alt in enumerate(alts[:max(1,int(top_k))]):
        dec=decisions[i] if isinstance(decisions,list) and i<len(decisions) else None
        r=iterate_alternative(alt,dec,weights); r["alternative_index"]=i; results.append(r)
    return {"engine":"TAKWEEN Design Iteration Engine","version":"3.9","alternatives_count":len(alts),"iterations":results,"note":"Applies bounded explainable edits and measures before/after impact; not final design approval."}
