# DTF Club Rulebook

Filterable league rulebook: every rule proposal 2019–2026 (type, year instituted, status, search),
plus scoring and league settings pulled live from Sleeper, with distinctive rules highlighted.

- `index.html` – the whole app (no build step). Config block at top of the script.
- `data/rules.json` – rule history, generated from `tools/rules.txt` (pipe-delimited; edit that, then `python3 tools/build.py`).
- `data/sleeper_snapshot.json` – offline fallback of the Sleeper league object.

Run: `python3 -m http.server` then open http://localhost:8000.
Add a rule: append a line to `tools/rules.txt` (`year|cat|status|title|nominator|impact|vote|note`).
Categories: SC RO IR TR PL SA DR MN GV FUN. Statuses: PASS FAIL PENDING TABLED EXPLORE WITHDRAWN.
