# DTF Club Rulebook

Filterable league rulebook: every rule proposal 2019–2026 (type, year instituted, status, search),
plus scoring and league settings pulled live from Sleeper, with distinctive rules highlighted.

- `index.html` – the whole app (no build step). Config block at top of the script.
- `tools/current.txt` – current rules from the league Site (`cat|year|group|rule|note`); `tools/rules.txt` – proposal history. Edit these, then run the build.
- `data/*.json` – generated.
- `data/sleeper_snapshot.json` – offline fallback of the Sleeper league object.

Build: `python3 tools/build.py` regenerates `data/rules.json` and a single-file `dist/rulebook.html` (rules and Sleeper snapshot inlined; still fetches live scoring from Sleeper when online, so it opens straight from disk). Dev: `python3 -m http.server`.
Add a rule: append a line to `tools/rules.txt` (`year|cat|status|title|nominator|impact|vote|note`).
Categories: SC RO IR TR PL SA DR MN GV FUN. Statuses: PASS FAIL PENDING TABLED EXPLORE WITHDRAWN.
