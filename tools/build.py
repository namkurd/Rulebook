"""Build: tools/*.txt -> data/*.json, plus standalone dist/rulebook.html (data inlined)."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..')

def lines(name):
    for l in open(os.path.join(here, name), encoding='utf-8'):
        l = l.rstrip('\n')
        if l and not l.startswith('#'):
            yield l

def dump(obj, name):
    json.dump(obj, open(os.path.join(root, 'data', name), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

rules = []
for l in lines('rules.txt'):
    y, c, s, t, n, im, v, no, flag, since = l.split('|')
    rules.append(dict(id=len(rules)+1, year=int(y), category=c, status=s, title=t, nominator=n, impact=im, vote=v, notes=no, flag=flag, since=int(since) if since else None))
dump(rules, 'rules.json')

cur = []
for l in lines('current.txt'):
    c, y, g, t, n = l.split('|')
    cur.append(dict(id=len(cur)+1, category=c, year=int(y) if y else None, group=g, rule=t, notes=n, source='site'))
# every passed rule still in force (not superseded, not a duplicate of a Site rule, not a one-time action)
for r in sorted(rules, key=lambda r: r['year']):
    if r['status'] == 'PASS' and not r['flag']:
        cur.append(dict(id=len(cur)+1, category=r['category'], year=r['since'] or r['year'], group='', rule=r['title'], notes=r['notes'], source='history'))
for i, r in enumerate(cur):
    r['id'] = i + 1
dump(cur, 'current_rules.json')
print(len(rules), 'history entries,', len(cur), 'current rules')

# standalone bundle
def raw(name):
    return open(os.path.join(root, 'data', name), encoding='utf-8').read().replace('</', '<\\/')
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
inline = "const INLINE={rules:%s,current:%s,snapshot:%s};\n" % (raw('rules.json'), raw('current_rules.json'), raw('sleeper_snapshot.json'))
html = html.replace("const CONFIG = {", inline + "const CONFIG = {", 1)
html = html.replace("getJSON(CONFIG.currentUrl),", "Promise.resolve(INLINE.current),", 1)
html = html.replace("getJSON(CONFIG.rulesUrl),", "Promise.resolve(INLINE.rules),", 1)
html = html.replace("getJSON(CONFIG.snapshotUrl).then(d=>[d,false])", "Promise.resolve([INLINE.snapshot,false])", 1)
os.makedirs(os.path.join(root, 'dist'), exist_ok=True)
for n in ('rulebook.html', 'index.html'):
    open(os.path.join(root, 'dist', n), 'w', encoding='utf-8').write(html)
print('wrote dist/rulebook.html', len(html)//1024, 'KB')
