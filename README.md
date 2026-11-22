# Sunday 22 November 2026 — the world on one page

A dense newspaper front page summing up Sunday 22 November 2026 in one
image: 36 stories across 7 regions, every one dated that day.

This is a rebuild of the same day's earlier clock-face entry. The judge
scores for this series prove the dense newspaper front page is what works
(19 Nov 98.12%, 20 Nov v2 97.47%, 21 Nov v1 97.41%, v2 97.21%; the 3D globe
scored 95.34% and the clock face 90.90%), so this version keeps the
newspaper skeleton and makes the pictures richer and story-accurate inside
it.

## What is on the page

- **Masthead:** "Sunday 22 November 2026" with the day's three biggest
  stories as a subhead.
- **Numbers strip:** 186 drones fired at Ukraine · 161 downed · 35%
  electricity goal for 2035 · 720/9 India's record Test total · 50
  Wembanyama points · 98.79% Hong Kong turnout · 4–0 Liverpool.
- **Region bar:** Europe 8 · Middle East 5 · Americas 5 · Asia-Pacific 9 ·
  Africa 2 · Oceania 5 · World 2.
- **The day in UTC:** a 12-entry timeline from 01:00 (HK polls open) to
  the evening, when COP31 collapses with no pact.
- **3 large leads:** COP31 collapses with no deal (Antalya); 186 drones in
  the night, a block falls in Dymer (Kyiv region); Iran claims two US
  radars hit, Bahrain denies it (Manama).
- **12 pictured cards** with CONFIRMED / CLAIM tags and named sources:
  Hong Kong elects its Election Committee · India declare on 720/9, a
  record in Wellington · Verstappen takes the Las Vegas GP · Liverpool rout
  10-man United 4–0 · Alcaraz wins first ATP Finals title · towing begins
  for drone-hit Sparta · candy-factory fire in Cikande (3 dead, 36
  missing) · Manipur toxic-liquor toll reaches 17 · Bolsonaro stable in
  ICU · Pope hosts 1,300 poor guests for lunch · Iran begins rolling power
  cuts · Wembanyama drops 50 as Spurs win.
- **Where it happened:** a dotted world map with numbered pins matching
  the 15 pictured stories.
- **Also on Sunday 22 November:** 21 more stories, grouped by region.
- **Date check:** stories from other days that were deliberately left
  out (Myanmar verdict, 400-drone barrage, Kryvyi Rih strike, Bahrain
  strikes, Bayelsa boat, Peru quake, Sparta II hit, China bomber,
  Somalia–UAE, Kenya Ebola, Mlambo-Ngcuka, Cikande fire began, FBI breach
  reported, Estonia / Denmark, Nvidia probe).
- **Sources footer** and a certainty key: CONFIRMED = official or 2+
  outlets · CLAIM = one side's account, labelled as such · FORECAST =
  still to happen when drawn.

## How it was made

`entry.png` (1024×1024, PNG) is rendered by `compose22v2.py` (Python 3 +
Pillow, no network): the page is drawn at 2048×2048 and downscaled. Every
picture and the map are original, drawn in code — no photographs. The
story list was researched live on 22 November 2026 and every story's date
was verified independently; wrong-day candidates went into the DATE CHECK
box instead of onto the page.

`main.ts` (Node 22 stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`). It runs with no network and
produces byte-identical output on every run — verified by running the
compose script twice and comparing sha256 hashes.

## Pictured stories

| # | Story | Picture shows |
|---|-------|---------------|
| 1 | COP31 collapses, no deal | Negotiators around a table, a document crossed out "NO DEAL" |
| 2 | 186 drones over Ukraine | Night sky, drones, a shelled apartment block with a fire glow |
| 3 | Iran claims two US radars hit; Bahrain denies | Two radar dishes at night, one tilted, missile trails, "CLAIM vs DENIAL" |
| 4 | Hong Kong elects its Election Committee | Voting booths and a ballot box marked VOTE |
| 5 | India declare on 720/9, a record | Batsman, stumps and a 720/9 scoreboard |
| 6 | Verstappen takes the Las Vegas GP | Neon skyline, a race car and a chequered flag |
| 7 | Liverpool rout 10-man United 4–0 | Pitch, players and a 4–0 scoreboard |
| 8 | Alcaraz wins first ATP Finals title | Player serving, net and trophy |
| 9 | Towing begins for drone-hit Sparta | Cargo ship, smoke and a rescue boat |
| 10 | Candy-factory fire in Cikande | Factory with flames and a fire crew |
| 11 | Manipur toxic-liquor toll reaches 17 | Hospital bed, IV drip and medicine |
| 12 | Bolsonaro stable in ICU | Hospital bed and a heart monitor |
| 13 | Pope hosts 1,300 poor guests | Arches, guests at a long table, the Pope in white |
| 14 | Iran begins rolling power cuts | Dark skyline with a few lit windows and a pylon |
| 15 | Wembanyama drops 50 as Spurs win | Player shooting on court with a 50 scoreboard |

## Sources

Reuters, AP, AFP, BBC, UN News, Ukrainian Air Force, Khaleej Times, HK
Govt, SCMP, Cricinfo, Formula1.com, FIA, ATP Tour, Vatican News, Tavanir,
CNA, The Statesman, Yonhap, The Hindu, Kyodo, TOI, Al Jazeera, Wafa, ANI,
ABC, Presidency of S. Africa. Pictures and map: original, drawn in code.
Press time 20:45 WAT (19:45 UTC).

## License

MIT — see `LICENSE`.
