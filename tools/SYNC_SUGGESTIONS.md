# Sync new suggestions from Slack

New league suggestions are added to the **Open suggestions** tab when Ben (Slack user `UCF97BSU9`)
reacts to a post in `#league-suggestions` (channel `CCG47441Z`, workspace dtf-club) with the 📖 `:book:` emoji.

## Procedure
1. Read the last ~30 days of `#league-suggestions` (`slack_read_channel`, paginate). Keep top-level posts that
   have a `book` reaction; confirm Ben reacted with `slack_get_reactions` (ignore book reactions from anyone else).
2. Permalink = `https://dtf-club.slack.com/archives/CCG47441Z/p<ts without the dot>`.
   **Skip** any post whose permalink already appears in `tools/rules.txt` (last column). Also read the post's
   thread (`slack_read_thread`) for context when the text is a short reply.
3. If the post is the same idea as an existing 2026 row, just add the permalink to that row's `link` column.
   Otherwise append a new line to `tools/rules.txt`:
   `YEAR|CAT|PENDING|short title|nominator first name|impact (blank if unknown)||note (quote or one-line context)|||permalink`
   - YEAR = the year of the newest `PENDING` section already in the file (2026 for now).
   - CAT = SC scoring, RO roster/lineup, IR injuries, TR waivers/FAB/trades, PL playoffs/standings, SA sacko,
     DR draft/auction, MN money, GV governance, FUN shotgun/fun.
   - Never edit or delete other rows; never invent votes or impact ratings.
4. Run `python3 tools/build.py`, check `git diff --stat`, commit to `main`, push. GitHub Pages serves the repo root.
5. Report which posts were added (or "nothing new").

Votes/outcomes are updated by hand from the League Suggestions sheet: change `PENDING` to `PASS`/`FAIL`, fill the vote
column, then rebuild.
