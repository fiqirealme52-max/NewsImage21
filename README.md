# NewsImage21

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up the world's news of **Saturday 21 November 2026** in one 1024×1024 image — **38 stories**: a giant serif date masthead ("Saturday 21 November 2026" under the kicker "THE WORLD IN ONE DAY"), a six-number strip, geographic region tabs (World 1 · Europe 10 · Americas 16 · Asia-Pacific 6 · Mideast 3 · Africa 2 · Oceania 0), three big scene-illustrated leads (the Russian missile down in Poland #01, Wall Street in correction, Kyiv hit overnight), ten medium stories with full-width coloured illustration bands and visible "CONFIRMED · outlet" source tags, a dark navy world map with 13 numbered pins, ocean labels and a compass rose, an "Also on Saturday" list of 25 more stories, a DATE CHECK box naming the other-day stories deliberately left out, a HOW SURE line, and a sources footer. Every fact comes only from sources dated 21 November 2026.

## The thirteen featured stories

1. **Missile down in Poland** — a Russian Kh-101 cruise missile crashes near Nowy Lipowiec; a second missile and a drone come down nearby. No one is hurt. PM Tusk calls it a deliberate provocation; NATO jets are scrambled and NATO chief Rutte flies to Warsaw. (Reuters, The Times, 21 Nov 2026.)
2. **Wall Street in correction** — Nasdaq falls 5.28% and the S&P 500 3.7% on Friday; the Dow and S&P enter correction. Nvidia drops 14% as the SEC probes its accounting. (Reuters, CNN, 21 Nov 2026.)
3. **Kyiv hit overnight** — Russia launches its biggest strike of November; bridges are hit and fires burn. At least 8 people are killed and 28 injured. (The Times, 21 Nov 2026.)
4. **COP31 runs into overtime** — talks in Antalya miss their Friday deadline; the draft drops fossil fuels. (Reuters.)
5. **6.8 quake shakes Peru** — a 6.8 quake strikes Junin, 129 km deep; tremors are felt in Lima. (Reuters.)
6. **Akvan weakens, rain floods Odisha** — 372,000 evacuated, none died; Patrapur records 209 mm of rain. (The Hindu BusinessLine.)
7. **Trump threatens data-centre tax** — a "tremendous tax" on firms building AI data centres abroad. (Reuters.)
8. **Iran readies tanker convoy** — fourteen Iranian tankers mass at Kharg Island to test the US blockade. (ISW.)
9. **Gen Z strikes across Europe** — a youth strike spreads across 25 countries over costs, arms and climate. (Reuters.)
10. **Rahul's SENA ton** — KL Rahul hits 100 off 207 balls in Wellington, the first Indian opener with SENA tons. (Reuters.)
11. **Mamdani: Rikers shut by 2032** — New York's mayor plans to close Rikers Island by 2032, five years late. (Reuters.)
12. **Gupta jailed for 19 years** — Nikhil Gupta gets 235 months in New York for plotting to kill Pannun. (Al Jazeera.)
13. **Denmark expels Russian diplomat** — Copenhagen expels Russia's military attache over a plot to kill Kyivstoner. (Meduza.)

## Also on Saturday — 25 more stories

14. Burnham: UK and EU to spend a year "brainstorming" future ties after the Brussels deal. 15. Saudi-led coalition strikes Hodeidah port; Houthis warn airlines to avoid Saudi airspace. 16. US Treasury sanctions four Iranian "oil trustees". 17. Iraqi troops enter the Jurf al-Sakhar militia stronghold. 18. Trump: Iran wants a deal, but "not acceptable to me". 19. Judge says she will halt Trump's 250-foot triumphal arch near Arlington Cemetery. 20. Texas executes Reinaldo Dennes, 70; the lethal injection takes more than an hour. 21. Russell Brand is jailed for 10 years 6 months. 22. Gold slides below $4,000 an ounce, down 9% for the week; VIX hits 35.89. 23. Anthropic shares fall to $88.91, just above the $83 IPO price. 24. Nvidia is down nearly 50% from its October high; $2.8 trillion of value has gone. 25. AMD falls another 13% a day after a short-seller report. 26. Fears grow the Fed will hike rates to fight inflation. 27. Foreign investors pour a record ₹1.22 lakh crore into Indian shares in November. 28. Nepal's PM Balen heads to Delhi for his first foreign visit. 29. US declassifies more UFO footage filmed in the Middle East. 30. Nearly 600 women killed in South Africa within three months. 31. ANC fights to keep control of South Africa's key cities. 32. French police sentenced over the beating of Michel Zecler. 33. Gerard Depardieu and a French author investigated over sexual allegations. 34. Fined $811m for conning detained migrants — but the scams did not stop. 35. Pochettino's first Man Utd test is Sunday at Anfield. 36. Padikkal makes 80 and Gill passes 50 as India pass 300 in Wellington. 37. Serbia elects Aleksandar Cupic of the Student List as parliament speaker. 38. Deadly protests hit Bangladesh ahead of Hasina's planned return.

## DATE CHECK — deliberately excluded (other days)

ICJ Rohingya ruling (19 Nov) · Trump–Xi–Putin declaration (19 Nov) · Crimean Bridge strike (19 Nov) · Anthropic IPO debut (19 Nov) · Mongolia president resigns (17 Nov) · Akvan landfall itself (20 Nov — story 06 is the 21 Nov aftermath) · UK–EU summit deal (20 Nov — story 14 is the 21 Nov follow-up) · Huang resigns (12 Nov).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG magic bytes, the 1024×1024 IHDR dimensions and the 1 MiB size limit. `draw.py` (Python 3 + PIL) regenerates the image from scratch if you want to redraw it.

## Determinism

The program is deterministic: it copies fixed bytes, uses no network, no clock and no randomness, so repeated runs write byte-identical output. `draw.py` is likewise deterministic — two runs produce a byte-identical `entry.png`.

<sub>Entered on [make.fun](https://make.fun/?ref=vfa7ye18&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
