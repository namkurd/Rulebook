import json,os
here=os.path.dirname(os.path.abspath(__file__));rows=[]
for l in open(os.path.join(here,'rules.txt'),encoding='utf-8'):
    l=l.rstrip('\n')
    if not l or l.startswith('#'):continue
    y,c,s,t,n,im,v,no=l.split('|')
    rows.append(dict(id=len(rows)+1,year=int(y),category=c,status=s,title=t,nominator=n,impact=im,vote=v,notes=no))
json.dump(rows,open(os.path.join(here,'..','data','rules.json'),'w',encoding='utf-8'),indent=1,ensure_ascii=False)
print(len(rows),'rules')
