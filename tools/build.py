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

import re
# Logical progression inside each section: (subsection label, regex on the rule text); first match in this order wins, last entry is the catch-all.
SUBS = {
 'SC': [('Receiving & first downs', r'ppr|first down'), ('Quarterback & turnovers', r'\bqb\b|fumble -0'), ('Kicking', r'kicker|extra point|\bxp'),
        ('Defense & special teams', r'4th down|defensive scoring|3-and-out|defense returning|tackle for loss|forced fumble|offense playing d'), ('Return yards', r'return')],
 'RO': [('Lineup slots', r'12-person|superflex|flex|te eligible|wr spot'), ('Bench & roster limits', r'bench|roster cap|cap\b'), ('Valid lineups', r'')],
 'IR': [('IR slots & eligibility', r'\bir\b|doubtful'), ('Injury replacement', r'')],
 'TR': [('Waivers, FAAB & transactions', r'waiver|faab|\bfab|free agent|no transactions'), ('Trades', r'')],
 'PL': [('Schedule', r'schedule'), ('Standings & tiebreakers', r'rumble|tiebreak|standings'), ('Playoff format & seeding', r'')],
 'SA': [('Bracket & qualification', r'toilet|outright|bracket|range'), ('Punishment', r'')],
 'DR': [('Auction & draft', r'')],
 'MN': [('Buy-in', r'buy-in'), ('Payouts', r'')],
 'GV': [('Platform & agreement', r'sleeper|abide'), ('Rule changes', r'(?!.*tanking)'), ('Conduct & fair play', r'')],
 'FUN': [('Shotgun', r'')],
}
CAT_ORDER = ['SC', 'RO', 'IR', 'TR', 'PL', 'SA', 'DR', 'MN', 'GV', 'FUN']
def classify(cat, text):
    subs = SUBS[cat]
    t = text.lower()
    if cat == 'GV':   # conduct only for tanking/collusion; everything else is rule-change process
        if re.search(r'sleeper|abide', t): return 0, subs[0][0]
        if re.search(r'tanking|collusion', t): return 2, subs[2][0]
        return 1, subs[1][0]
    for i, (label, rx) in enumerate(subs):
        if rx == '' or re.search(rx, t): return i, label
    return len(subs) - 1, subs[-1][0]

rules = []
for l in lines('rules.txt'):
    y, c, s, t, n, im, v, no, flag, since, link, by = l.split('|')
    rules.append(dict(id=len(rules)+1, year=int(y), category=c, status=s, title=t, nominator=n, impact=im, vote=v, notes=no, flag=flag, since=int(since) if since else None, link=link, by=by))
for r in rules:
    i, r['sub'] = classify(r['category'], r['title'])
    r['ord'] = CAT_ORDER.index(r['category']) * 100 + i
dump(rules, 'rules.json')

cur = []
for l in lines('current.txt'):
    parts = l.split('|')
    c, y, g, t, n = parts[:5]
    label = parts[5] if len(parts) > 5 else 'league site'
    cur.append(dict(id=len(cur)+1, category=c, year=int(y) if y else None, group=g, rule=t, notes=n, source='site', label=label))
# every passed rule still in force (not superseded, not a duplicate of a Site rule, not a one-time action)
for r in sorted(rules, key=lambda r: r['year']):
    if r['status'] == 'PASS' and not r['flag']:
        cur.append(dict(id=len(cur)+1, category=r['category'], year=r['since'] or r['year'], group='', rule=r['title'], notes=r['notes'], source='history', label='suggestions sheet'))
# superseded rules become footnotes on the rule that replaced them
for r in rules:
    if r['by']:
        tgt = [c for c in cur if c['rule'].startswith(r['by'])]
        assert len(tgt) == 1, ('no unique target for', r['title'], r['by'], len(tgt))
        tgt[0].setdefault('replaces', []).append(dict(year=r['year'], title=r['title'], notes=r['notes']))
for c in cur:
    c.get('replaces', []).sort(key=lambda x: -x['year'])
for i, r in enumerate(cur):
    r['id'] = i + 1
    j, r['sub'] = classify(r['category'], r['rule'])
    r['ord'] = CAT_ORDER.index(r['category']) * 100 + j
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
