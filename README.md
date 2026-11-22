# Sunday 22 November 2026 — The World in One Day, Told by the Clock

Entry for the make.fun bounty **"Sum up 22 November's world news in one image"**
(competition `news-image-20261122`).

## What the image shows

A warm, bright analogue clock face for Sunday 22 November 2026. The hands
stand at 1:00 — the hour this entry was drawn, as the day began — and the
centre of the dial carries the date. Ten of the day's stories are pictured as
illustrated medallions around the dial, a sun at 12 o'clock and a moon at 6.
A bottom band carries three more headlines, and a **DATE CHECK** box names
the big stories of 19–21 November that were deliberately left out, so the
page is about 22 November only.

Every pictured story happened, or was first reported, on Sunday 22 November
2026 in its own time zone. At the time of drawing (01:00 WAT) Europe and the
Americas had not yet had their 22nd, so the page leans on Asia-Pacific and
overnight news — that is by design.

## Pictured stories

| # | Story | Source |
|---|-------|--------|
| 1 | COP31 climate talks in Antalya close to a final deal; refined package presented at a late-night plenary in the early hours of Sunday; approval session set for 06:00 GMT | Arab News, 22 Nov 2026 04:40 PKT — https://www.arabnews.pk/world/cop31-climate-talks-close-to-final-deal-says-summit-president-3007719 |
| 2 | Formula 1 Las Vegas Grand Prix, race Sunday 22 Nov 04:00 UTC (Sat 20:00 PST); Verstappen on pole after Antonelli's grid penalty | Formula One History — https://www.formulaonehistory.com/2026-las-vegas-grand-prix/ |
| 3 | India vs New Zealand, 1st Test, Wellington, Day 4: Rishabh Pant century (120 off 142); India 616/5, their highest Test innings total in New Zealand | NDTV live blog, 22 Nov 2026 05:24 IST — https://sports.ndtv.com/new-zealand-vs-india-2026-27/india-vs-new-zealand-live-score-1st-test-day-4-ind-vs-nz-2026-cricket-match-updates-rishabh-pant-anshul-kamboj-12359965 |
| 4 | Sonepur Mela opens in Bihar: CM Samrat Choudhary inaugurates the month-long Harihar Kshetra fair (22 Nov–23 Dec), Asia's largest cattle fair | Times of India, 22 Nov 2026 — https://timesofindia.indiatimes.com/city/patna/cm-to-inaugurate-sonepur-mela-today/articleshow/136058706.cms |
| 5 | Netherlands Foreign Minister Tom Berendsen arrives in New Delhi on Sunday 22 Nov for a two-day visit; meets EAM S. Jaishankar on Sunday evening | The Tribune (ANI), 21 Nov dateline — https://www.tribuneindia.com/news/world/netherlands-fm-berendsen-to-visit-india-to-hold-talks-with-jaishankar-vaishnaw/ |
| 6 | US Senate Democrats' leadership fight: incoming class split between Chuck Schumer and challenger Chris Van Hollen ahead of the 1 Dec secret-ballot vote | AP analysis, 22 Nov 2026 — https://www.arabnews.pk/world/democrats-who-swept-into-the-senate-promised-change-a-leadership-vote-is-testing-them-early-3007717 |
| 7 | Ashes, 1st Test, Perth: Australia beat England by 8 wickets in two days; Travis Head 123 off 83, Mitchell Starc 10-wicket match haul | ANI, Perth, 22 Nov 2026 — https://usfijitimes.org/ashes-1st-test-head-reverses-bazball-card-on-engla |
| 8 | Britain's Prince William announces an insurance scheme for 10,000 temporary forest personnel | The Daily Jagran, 22 Nov 2026 school-assembly headlines — https://www.thedailyjagran.com/education/news/todays-school-assembly-news-headline-november-22-check-top-national-international-and-sports-news-here-10337156 |
| 9 | Air India and Air India Express extend the suspension of Jeddah flights till 24 November | The Daily Jagran, 22 Nov 2026 (same list as above) |
| 10 | ICMR completes 100 technology transfers and signs 20 licensing agreements at its Health Research Summit | The Daily Jagran, 22 Nov 2026 (same list as above) |

Also today (bottom band): Pat Cummins keeps Australia's Test captaincy
(Cricket Australia); Victoria votes Saturday 28 Nov, early voting centres
closed today; COP31 approval session 06:00 GMT; F1 Las Vegas race 04:00 UTC.

Deliberately excluded (DATE CHECK box): ICJ Myanmar verdict (19 Nov), Peru
quake (21 Nov), Houthi missiles on Riyadh (21 Nov), Trump card-rate vow
(21 Nov), Iran strikes on Bahrain (21 Nov), French protests (21 Nov),
Brazil storm (20 Nov), WFP outlook (20 Nov).

## How it was built

`compose22.py` (Python 3 + Pillow, DejaVu fonts) draws the whole image in
code — clock face, medallions, and every illustration are PIL primitives;
no photographs were used, and no network access is needed. The image is
rendered at 2x and downscaled to 1024×1024 for clean edges, and was
inspected at zoom before submission (two clipped scoreboards and hidden
Senate figures were caught and fixed).

## How to run

```sh
node main.ts            # copies entry.png to $MAKEFUN_OUTPUT_DIR (or /output)
```

`main.ts` uses only the Node 22 standard library. Two runs produce
byte-identical output (verified with `sha256sum`).

## Licence

MIT — see `LICENSE`.
