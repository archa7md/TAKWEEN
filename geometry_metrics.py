
from math import hypot
def metrics(project):
    rooms=[r for l in project.get("levels",[]) for r in l.get("rooms",[])]
    def c(r):
        g=r.get("geometry",{}); return (float(g.get("x",0))+float(g.get("w",0))/2,float(g.get("y",0))+float(g.get("h",0))/2)
    area=sum(float(r.get("geometry",{}).get("w",0))*float(r.get("geometry",{}).get("h",0)) for r in rooms)
    site=project.get("site_fit",{})
    env=float(site.get("width_m",0))*float(site.get("depth_m",0))
    efficiency=min(1,area/env) if env else .5
    if len(rooms)>1:
        ds=[hypot(c(rooms[i])[0]-c(rooms[i-1])[0],c(rooms[i])[1]-c(rooms[i-1])[1]) for i in range(1,len(rooms))]
        circulation=max(0,min(1,1-(sum(ds)/len(ds))/15))
    else: circulation=1
    private=[r for r in rooms if "bed" in r.get("name","").lower()]
    public=[r for r in rooms if any(x in r.get("name","").lower() for x in ["majlis","family","entrance","foyer"])]
    if private and public:
        d=[hypot(c(a)[0]-c(b)[0],c(a)[1]-c(b)[1]) for a in private for b in public]
        privacy=max(0,min(1,sum(d)/len(d)/12))
    else: privacy=.7
    daylight=min(1,(len(rooms)-1)/max(1,len(rooms)))
    adjacency=max(0,min(1,1-abs(len(rooms)-8)/16))
    envelope_fit=1 if env>=area and env else .5
    return {"area_efficiency":round(efficiency,4),"circulation":round(circulation,4),
            "privacy":round(privacy,4),"daylight":round(daylight,4),
            "adjacency":round(adjacency,4),"envelope_fit":round(envelope_fit,4),
            "gross_room_area_m2":round(area,2),"room_count":len(rooms)}
