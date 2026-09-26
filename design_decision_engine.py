"""TAKWEEN v3.8 - Explainable AI Design Decision Layer.

Deterministic decision-support layer over the v3.7 unified design intelligence.
It does not claim code compliance or replace architect review.
"""
from copy import deepcopy
from unified_design_engine import score_alternative, DEFAULT_WEIGHTS

LABELS = {
    "geometry": "geometry / envelope fit",
    "adjacency": "functional adjacency",
    "privacy": "privacy gradient",
    "efficiency": "area efficiency",
    "orientation": "site orientation",
    "multi_floor": "multi-floor organization",
    "site": "site response",
}

ACTION_RULES = {
    "privacy": "Increase separation between guest/public spaces and family/private rooms, and keep private rooms away from the main entrance path.",
    "adjacency": "Strengthen direct relationships between frequently paired spaces such as entrance–majlis, kitchen–dining, and family living–dining.",
    "geometry": "Refine room positions and dimensions to improve envelope fit and reduce geometric conflicts.",
    "efficiency": "Reduce unnecessary circulation and rebalance oversized or undersized spaces while preserving required functions.",
    "orientation": "Reconsider room placement against the recommended view, road, privacy, and daylight sides of the site.",
    "site": "Adjust zoning and openings to respond more clearly to road exposure, preferred views, and privacy sides.",
    "multi_floor": "Rebalance floor assignments so public functions remain accessible and private functions are grouped appropriately across levels.",
}


def _clamp(v):
    try:
        return max(0.0, min(1.0, float(v)))
    except Exception:
        return 0.0


def _ranked_factors(components, weights):
    rows = []
    for key, value in components.items():
        rows.append({
            "factor": key,
            "label": LABELS.get(key, key),
            "score": round(_clamp(value), 6),
            "weight": round(float(weights.get(key, 0)), 6),
            "weighted_contribution": round(_clamp(value) * float(weights.get(key, 0)), 6),
        })
    return sorted(rows, key=lambda x: (x["score"], x["weighted_contribution"]), reverse=True)


def _decision_from_score(score, weak_count, hard_issues=0):
    if hard_issues > 0:
        return "review"
    if score >= 0.72 and weak_count <= 1:
        return "retain"
    if score >= 0.55:
        return "revise"
    return "review"


def analyze_alternative(alternative, weights=None):
    """Return an explainable architectural decision for one alternative."""
    weights = dict(DEFAULT_WEIGHTS, **(weights or {}))
    scored = score_alternative(alternative, weights)
    components = scored["components"]
    factors = _ranked_factors(components, weights)
    strong = [f for f in factors if f["score"] >= 0.70][:3]
    weak = [f for f in sorted(factors, key=lambda x: x["score"]) if f["score"] < 0.55][:3]

    strengths = [
        f"{f['label'].capitalize()} is comparatively strong ({f['score']:.2f})."
        for f in strong
    ]
    issues = [
        f"{f['label'].capitalize()} is below the preferred review threshold ({f['score']:.2f})."
        for f in weak
    ]
    actions = [ACTION_RULES[f["factor"]] for f in weak if f["factor"] in ACTION_RULES]

    # Transparent heuristics for constraint-style review signals.
    hard_issues = 0
    geometry = scored.get("geometry_metrics", {})
    for key in ("overlap_count", "constraint_violations"):
        value = geometry.get(key)
        if isinstance(value, (int, float)) and value > 0:
            hard_issues += int(value)
    if isinstance(geometry.get("overlaps"), list) and geometry["overlaps"]:
        hard_issues += len(geometry["overlaps"])

    decision = _decision_from_score(scored["score"], len(weak), hard_issues)
    confidence = round(min(0.95, 0.55 + 0.05 * len(factors) + (0.10 if not hard_issues else 0.0)), 2)

    return {
        "engine": "TAKWEEN AI Design Decision Layer",
        "version": "3.8",
        "decision": decision,
        "score": scored["score"],
        "confidence": confidence,
        "summary": (
            "Retain with architect review of the identified factors."
            if decision == "retain" else
            "Revise the identified weak factors and re-run the analysis."
            if decision == "revise" else
            "Review geometry and design constraints before relying on this alternative."
        ),
        "strengths": strengths,
        "issues": issues,
        "recommended_actions": actions,
        "factor_trace": factors,
        "hard_issue_count": hard_issues,
        "source_metrics": {
            "components": deepcopy(components),
            "geometry_metrics": deepcopy(scored.get("geometry_metrics", {})),
            "villa_metrics": deepcopy(scored.get("villa_metrics", {})),
            "orientation_metrics": deepcopy(scored.get("orientation_metrics", {})),
            "vertical_metrics": deepcopy(scored.get("vertical_metrics", {})),
        },
        "limitations": [
            "Deterministic design-assistance heuristic; not a generative LLM judgment.",
            "Not a Saudi Building Code or municipality compliance verdict.",
            "Architect review remains required before design decisions are issued.",
        ],
    }


def design_decision(project, weights=None, top_k=6):
    """Analyze one or multiple alternatives and preserve traceability to v3.7."""
    alts = project.get("alternatives") if isinstance(project, dict) else None
    if not isinstance(alts, list):
        alts = [project]
    results = []
    for i, alt in enumerate(alts[:max(1, int(top_k))]):
        result = analyze_alternative(alt, weights)
        result["alternative_index"] = i
        results.append(result)
    return {
        "engine": "TAKWEEN AI Design Decision Layer",
        "version": "3.8",
        "alternatives_count": len(alts),
        "decisions": results,
        "weights": dict(DEFAULT_WEIGHTS, **(weights or {})),
        "note": "Explainable design assistance grounded in TAKWEEN v3.7 metrics; not code compliance or final architectural approval.",
    }
