import json,os
here=os.path.dirname(os.path.abspath(__file__));rows=[]
for l in open(os.path.join(here,'rules.txt'),encoding='utf-8'):
    l=l.rstrip('\n')
    if not l or l.startswith('#'):continue
    y,c,s,t,n,im,v,no=l.split('|')
    rows.append(dict(id=len(rows)+1,year=int(y),category=c,status=s,title=t,nominator=n,impact=im,vote=v,notes=no))
json.dump(rows,open(os.path.join(here,'..','data','rules.json'),'w',encoding='utf-8'),indent=1,ensure_ascii=False)
print(len(rows),'rules')

# --- standalone bundle: inline rules + Sleeper snapshot into one file (dist/rulebook.html) ---
root=os.path.join(here,'..')
html=open(os.path.join(root,'index.html'),encoding='utf-8').read()
snap=open(os.path.join(root,'data','sleeper_snapshot.json'),encoding='utf-8').read()
rules=open(os.path.join(root,'data','rules.json'),encoding='utf-8').read()
inline="const INLINE={rules:%s,snapshot:%s};\n"%(rules.replace('</','<\\/'),snap.replace('</','<\\/'))
html=html.replace("const CONFIG = {",inline+"const CONFIG = {",1)
html=html.replace("getJSON(CONFIG.rulesUrl),","Promise.resolve(INLINE.rules),",1)
html=html.replace("getJSON(CONFIG.snapshotUrl).then(d=>[d,false])","Promise.resolve([INLINE.snapshot,false])",1)
os.makedirs(os.path.join(root,'dist'),exist_ok=True)
open(os.path.join(root,'dist','rulebook.html'),'w',encoding='utf-8').write(html)
print('wrote dist/rulebook.html',len(html)//1024,'KB')
