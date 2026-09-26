
"""TAKWEEN v3.2 - deterministic architectural constraint solver.

This module performs bounded local-search layout refinement. It is intentionally
dependency-free and deterministic. It improves an existing alternative rather
than claiming a global optimum.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import math

@dataclass
class SolveConfig:
    iterations: int = 160
    step_m: float = 0.25
    size_step_m: float = 0.25
    top_k: int = 3

def _rooms(alt: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("rooms", "spaces", "program"):
        v = alt.get(key)
        if isinstance(v, list):
            return v
    return []

def _xywh(r):
    x = float(r.get("x", r.get("x_m", 0)))
    y = float(r.get("y", r.get("y_m", 0)))
    w = float(r.get("w", r.get("width", r.get("width_m", 0))))
    h = float(r.get("h", r.get("depth", r.get("height", r.get("depth_m", 0)))))
    return x, y, w, h

def _setxywh(r, x, y, w, h):
    for k in ("x", "x_m"):
        if k in r: r[k] = round(x, 3)
    for k in ("y", "y_m"):
        if k in r: r[k] = round(y, 3)
    for k in ("w", "width", "width_m"):
        if k in r: r[k] = round(w, 3)
    for k in ("h", "depth", "height", "depth_m"):
        if k in r: r[k] = round(h, 3)

def _area(r):
    _, _, w, h = _xywh(r)
    return max(0.0, w*h)

def _overlap(a,b):
    ax,ay,aw,ah=_xywh(a); bx,by,bw,bh=_xywh(b)
    ix=max(0.0, min(ax+aw,bx+bw)-max(ax,bx))
    iy=max(0.0, min(ay+ah,by+bh)-max(ay,by))
    return ix*iy

def _bounds(alt):
    # Accept common envelope shapes used in TAKWEEN versions.
    for key in ("envelope", "buildable_envelope", "site", "plot"):
        e=alt.get(key)
        if isinstance(e,dict):
            w=e.get("width_m",e.get("width",e.get("w")))
            h=e.get("depth_m",e.get("depth",e.get("h")))
            if w is not None and h is not None:
                return float(w),float(h)
    w=alt.get("envelope_width_m",alt.get("site_width_m",alt.get("width_m")))
    h=alt.get("envelope_depth_m",alt.get("site_depth_m",alt.get("depth_m")))
    if w is not None and h is not None: return float(w),float(h)
    return None

def _constraint_report(alt):
    rooms=_rooms(alt)
    bounds=_bounds(alt)
    violations=[]
    min_clear=float(alt.get("min_clearance_m",0.10))
    for r in rooms:
        name=r.get("name",r.get("id","room"))
        x,y,w,h=_xywh(r)
        min_area=float(r.get("min_area_m2",r.get("min_area",0)) or 0)
        max_area=float(r.get("max_area_m2",r.get("max_area",1e9)) or 1e9)
        min_w=float(r.get("min_width_m",r.get("min_width",0)) or 0)
        min_h=float(r.get("min_depth_m",r.get("min_height_m",r.get("min_depth",0))) or 0)
        if _area(r) < min_area-1e-6:
            violations.append({"type":"min_area","room":name,"amount":round(min_area-_area(r),3)})
        if _area(r) > max_area+1e-6:
            violations.append({"type":"max_area","room":name,"amount":round(_area(r)-max_area,3)})
        if w < min_w-1e-6:
            violations.append({"type":"min_width","room":name,"amount":round(min_w-w,3)})
        if h < min_h-1e-6:
            violations.append({"type":"min_depth","room":name,"amount":round(min_h-h,3)})
        if bounds:
            W,H=bounds
            if x < -1e-6 or y < -1e-6 or x+w > W+1e-6 or y+h > H+1e-6:
                violations.append({"type":"envelope","room":name})
    for i,a in enumerate(rooms):
        for b in rooms[i+1:]:
            ov=_overlap(a,b)
            if ov > min_clear*min_clear:
                violations.append({"type":"overlap","rooms":[a.get("name",a.get("id")),b.get("name",b.get("id"))],"area":round(ov,3)})
    return violations

def _fallback_score(alt):
    # A simple structural score if the caller does not supply a scorer.
    violations=_constraint_report(alt)
    return -1000*len(violations)

def solve_alternative(alternative: Dict[str, Any], scorer=None, config: SolveConfig|None=None):
    """Refine one alternative. Returns solved alternative + before/after report."""
    cfg=config or SolveConfig()
    score_fn=scorer or _fallback_score
    current=deepcopy(alternative)
    before_report=_constraint_report(current)
    before_score=float(score_fn(current))
    best=deepcopy(current); best_score=before_score

    rooms=_rooms(best)
    bounds=_bounds(best)
    for _ in range(max(1,cfg.iterations)):
        improved=False
        for i,r0 in enumerate(list(_rooms(best))):
            # Deterministic candidate sequence: translations then size changes.
            x,y,w,h=_xywh(r0)
            candidates=[]
            for dx,dy in ((cfg.step_m,0),(-cfg.step_m,0),(0,cfg.step_m),(0,-cfg.step_m)):
                candidates.append((x+dx,y+dy,w,h))
            for dw,dh in ((cfg.size_step_m,0),(-cfg.size_step_m,0),(0,cfg.size_step_m),(0,-cfg.size_step_m)):
                candidates.append((x,y,w+dw,h+dh))
            for nx,ny,nw,nh in candidates:
                if nw <= 0 or nh <= 0: continue
                trial=deepcopy(best)
                tr=_rooms(trial)[i]
                _setxywh(tr,nx,ny,nw,nh)
                # Hard feasibility guards for dimensions/envelope/overlap.
                if _constraint_report(trial):
                    # Allow moves that reduce violations only.
                    old_v=len(_constraint_report(best))
                    new_v=len(_constraint_report(trial))
                    if new_v > old_v: continue
                s=float(score_fn(trial))
                if s > best_score + 1e-9:
                    best, best_score = trial, s
                    improved=True
        if not improved:
            break

    after_report=_constraint_report(best)
    result=deepcopy(best)
    result["solver_v3_2"]={
        "method":"deterministic_bounded_local_search",
        "iterations":cfg.iterations,
        "step_m":cfg.step_m,
        "before_score":round(before_score,6),
        "after_score":round(best_score,6),
        "score_delta":round(best_score-before_score,6),
        "violations_before":len(before_report),
        "violations_after":len(after_report),
        "constraint_status":"PASS" if not after_report else "REVIEW",
    }
    return result, {
        "before_score":before_score,
        "after_score":best_score,
        "before_violations":before_report,
        "after_violations":after_report,
    }

def solve_project(alternatives: List[Dict[str, Any]], scorer=None, config=None):
    solved=[]
    for alt in alternatives:
        s, report=solve_alternative(alt, scorer=scorer, config=config)
        solved.append(s)
    solved.sort(key=lambda a:a.get("solver_v3_2",{}).get("after_score",-1e18), reverse=True)
    return solved
