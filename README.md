# NewsImage21

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up the world's news of **Saturday 21 November 2026** in one 1024×1024 image — **38 stories**: a giant serif date masthead ("Saturday 21 November 2026" under the kicker "THE WORLD IN ONE DAY"), a six-number strip, geographic region tabs (World 1 · Europe 12 · Americas 14 · Asia-Pacific 3 · Mideast 3 · Africa 3 · Oceania 2), three big scene-illustrated leads (COP31 runs into overtime #01, Riyadh intercepts #02, Kryvyi Rih strikes #03), ten medium stories with real full-width scene illustration bands and visible "CONFIRMED · outlet" source tags, a dark navy world map with 13 numbered pins, ocean labels and a compass rose, an "Also on Saturday" list of 25 more stories, a DATE CHECK box naming the Friday 20 November news deliberately left out, a HOW SURE line, and a sources footer. Every fact comes only from sources dated 21 November 2026.

## The thirteen featured stories

1. **COP31 runs into overtime** — talks in Antalya miss their Friday deadline; the draft drops fossil fuels and the $120bn adaptation target. (Reuters, Le Monde, 21 Nov 2026.)
2. **Riyadh intercepts** — coalition air defences down 3 Houthi ballistic missiles over Riyadh in the early hours; 2 more fall over Jizan. (Reuters, AFP.)
3. **Kryvyi Rih strikes** — a Russian missile hits a restaurant in Kryvyi Rih on Friday night. A boy, 7, and a paramedic die; 42 are hurt. (Kyiv Independent, Ukrainska Pravda.)
4. **BepiColombo reaches Mercury** — after 8 years, ESA and JAXA's twin orbiters reach Mercury's orbit today. (ESA, Sky & Telescope.)
5. **Rutte flies to Warsaw** — NATO chief heads to Warsaw for talks with PM Tusk. (Reuters, The Times.)
6. **6.7 quake shakes Peru** — a 6.7 quake strikes Junin, 108 km deep (USGS); tremors are felt in Lima. (AFP, Reuters.)
7. **US clears 879,868 AI chips** — Commerce approves 879,868 Nvidia and AMD AI chips for China. (Reuters.)
8. **Coalition hits Hodeidah port** — Saudi-led forces strike Hodeidah port and targets in Sanaa and Saada. (Reuters.)
9. **EU hands Kyiv €7.9bn** — Brussels disburses €7.9bn to Ukraine, its largest-ever single payment. (European Commission, Reuters.)
10. **Rahul's SENA ton** — KL Rahul makes 136 as India reach 486/4 at stumps, leading NZ by 118. (ESPNcricinfo, Reuters.)
11. **Verstappen takes Vegas pole** — Antonelli is fastest but a 5-place penalty hands pole to Verstappen. (Formula 1, Reuters.)
12. **Medvedev meets Zverev tonight** — two former champions meet tonight in Turin. Medvedev leads 14-8. (ATP Tour.)
13. **Denmark charges two over plot** — two men are charged over a plot to kill rapper Kyivstoner. (Reuters, BBC.)

## Also on Saturday — 25 more stories

14. Burnham: a year of "brainstorming" EU ties. 15. Funeral boat capsizes in Bayelsa; 4 dead. 16. US sanctions four Iranian "oil trustees". 17. Iraqi troops enter Jurf al-Sakhar stronghold. 18. Trump: Iran wants a deal, "not acceptable". 19. Judge will halt Trump's 250-foot arch. 20. Texas executes Dennes, 70. 21. Russell Brand jailed 10 years 6 months. 22. Gold below $4,000; VIX at 35.89, a 19-month high. 23. Anthropic shares fall to $88.91. 24. Nvidia down nearly 50% from October high. 25. AMD falls 13% after a short-seller report. 26. Fears grow the Fed will hike rates. 27. Record ₹1.22 lakh crore into Indian shares. 28. Nepal PM Balen heads to Delhi. 29. US declassifies more UFO footage from the Mideast. 30. Nearly 600 women killed in South Africa in 3 months. 31. ANC fights to keep control of key South African cities. 32. French police sentenced over Zecler beating. 33. Depardieu investigated over sex allegations. 34. Fined $811m for conning detained migrants. 35. Pochettino's first Man Utd test is Sunday. 36. Padikkal 80, Gill 50+ as India pass 300. 37. Serbia elects Cupic as parliament speaker. 38. Deadly protests hit Bangladesh ahead of return.

## DATE CHECK — deliberately excluded (other days)

Left out as Friday 20 November's news: Russian missiles land in Poland · Kyiv bridges hit · Wall Street enters correction · Cyclone Akvan landfall · UK–EU summit deal. Thursday 19 November: ICJ Rohingya ruling · Trump–Xi–Putin declaration · Crimean Bridge strike · Anthropic IPO debut · Mongolia president resigns (17 Nov) · Huang resigns (12 Nov). Not yet happened: COP31 final deal · Las Vegas GP race · BepiColombo science phase · ATP Finals final.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG magic bytes, the 1024×1024 IHDR dimensions and the 1 MiB size limit. `draw.py` (Python 3 + PIL) regenerates the image from scratch if you want to redraw it.

## Determinism

The program is deterministic: it copies fixed bytes, uses no network, no clock and no randomness, so repeated runs write byte-identical output. `draw.py` is likewise deterministic — two runs produce a byte-identical `entry.png`.

<sub>Entered on [make.fun](https://make.fun/?ref=vfa7ye18&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
