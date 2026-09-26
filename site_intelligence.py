from dataclasses import dataclass,asdict
@dataclass
class Site:
 width_m:float; depth_m:float; north_deg:float=0; frontage:str='street'; setbacks:dict=None
 def __post_init__(self): self.setbacks=self.setbacks or {'front':5,'rear':3,'left':2,'right':2}
 @property
 def buildable_width_m(self): return max(0,self.width_m-self.setbacks['left']-self.setbacks['right'])
 @property
 def buildable_depth_m(self): return max(0,self.depth_m-self.setbacks['front']-self.setbacks['rear'])

def normalize_site(d):
 s=Site(float(d.get('width_m',20)),float(d.get('depth_m',30)),float(d.get('north_deg',0)),str(d.get('frontage','street')),{k:float((d.get('setbacks') or {}).get(k,v)) for k,v in {'front':5,'rear':3,'left':2,'right':2}.items()})
 return {'site':asdict(s),'derived':{'site_area_m2':s.width_m*s.depth_m,'buildable_width_m':s.buildable_width_m,'buildable_depth_m':s.buildable_depth_m,'buildable_area_m2':s.buildable_width_m*s.buildable_depth_m}}
