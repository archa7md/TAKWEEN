
DEFAULT={"privacy":.2,"adjacency":.2,"circulation":.15,"efficiency":.15,"orientation":.1,"parking":.1,"daylight":.1}
def optimize(alts,weights=None,metric_fn=None):
    w=dict(DEFAULT); w.update(weights or {})
    total=sum(max(0,v) for v in w.values()) or 1
    w={k:v/total for k,v in w.items()}
    out=[]
    for a in alts:
        m=metric_fn(a) if metric_fn else a.get("scores",{})
        f={"privacy":m.get("privacy",.7),"adjacency":m.get("adjacency",.7),
           "circulation":m.get("circulation",.7),"efficiency":m.get("area_efficiency",m.get("efficiency",.7)),
           "orientation":m.get("orientation",.7),
           "parking":.75 if a.get("parking",0)>=2 else .55,
           "daylight":m.get("daylight",.7)}
        s=sum(f[k]*w.get(k,0) for k in f)
        x=dict(a); x["geometry_metrics"]=m; x["optimization"]={"factors":f,"weighted_score":round(s,4)}
        out.append(x)
    out.sort(key=lambda x:x["optimization"]["weighted_score"],reverse=True)
    for i,x in enumerate(out,1): x["optimization"]["rank"]=i
    return {"engine_version":"3.1","mode":"geometry-based","weights":w,"alternatives":out}
