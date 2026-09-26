"""Input/output validation for TAKWEEN Final MVP."""

def validate_request(payload):
    errors=[]
    if not isinstance(payload,dict): return ["Request body must be an object"]
    site=payload.get("site",{})
    for k in ("width_m","depth_m"):
        if k in site:
            try:
                if float(site[k]) <= 0: errors.append(f"site.{k} must be > 0")
            except Exception: errors.append(f"site.{k} must be numeric")
    count=payload.get("count",8)
    try:
        if not 1 <= int(count) <= 12: errors.append("count must be between 1 and 12")
    except Exception: errors.append("count must be an integer")
    return errors

def validate_result(result):
    required=("product","version","brief","site","generative_design","selected_alternative","bim","physical_bim","boq","ifc")
    missing=[k for k in required if k not in result]
    return {"valid":not missing,"missing":missing}
