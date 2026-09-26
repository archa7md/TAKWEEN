import re
def parse_brief(t):
 def num(p,d):
  m=re.search(p,t,re.I); return int(m.group(1)) if m else d
 return {'source':'local-deterministic-parser','language':'ar' if re.search(r'[\u0600-\u06ff]',t) else 'en','requirements':{'bedrooms':num(r'(\d+)\s*(?:bedroom|bedrooms|غرفة نوم|غرف نوم)',4),'floors':num(r'(\d+)\s*(?:floor|floors|دور|أدوار)',2),'parking':num(r'(\d+)\s*(?:parking|مواقف|سيارات)',2),'city':'Jeddah' if re.search('جدة|jeddah',t,re.I) else None,'raw_text':t}}
