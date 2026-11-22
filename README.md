# NewsImage21

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/fiqirealme52-max/NewsImage21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up the world's news of **Saturday 21 November 2026** in one 1024×1024 image — **35 stories**: a giant serif date masthead ("Saturday 21 November 2026" under the kicker "THE WORLD IN ONE DAY"), a "THE DAY IN UTC" timeline of 7 timed events, a six-number strip, geographic region tabs (Europe 8 · Middle East 6 · Americas 5 · Asia 9 · Oceania 3 · Africa 1 · Global 3), three big scene-illustrated leads (COP31 runs into overtime #01, Iran strikes Bahrain #02, Peru quake #03), ten medium stories with real full-width scene illustration bands and visible source strips, a light world map with 11 numbered pins (No. 9 is a world market, No. 13 is in space), an "Also on Saturday" list of 22 more stories, a DATE CHECK box naming the Friday 20 November news deliberately left out, a HOW WE CHECKED line, and a sources footer. Every fact comes only from sources dated 21 November 2026.

## The thirteen featured stories

1. **COP31 runs into overtime** — talks in Antalya miss their Friday deadline; the draft drops fossil fuels and the $120bn adaptation target. (Reuters, AFP, 21 Nov 2026.)
2. **Iran strikes Bahrain bases** — IRGC says it hit US radar at two bases; Bahrain says a civilian plant burned; two tankers struck off Khasab. (Al Jazeera, Xinhua, UKMTO.)
3. **Deep 6.7 quake shakes Peru** — centred near Carhuamayo, felt in Lima; no deaths, no tsunami risk. USGS 108 km deep; IGP 129 km. (USGS, IGP.)
4. **Three Houthi missiles shot down over Riyadh** — coalition says three ballistic missiles destroyed before dawn; two more fell over Jizan on Friday evening. (Reuters, AFP.)
5. **Mexico captures cartel boss 'El Chapo Isidro'** — FBI top-10 fugitive seized in Guasave; 11 die in clashes. (Reuters, AP.)
6. **EU and Indonesia sign trade pact** — signed in Brussels after a decade of talks; 98.5% of EU lines and 90.4% of Indonesian lines go duty-free. (Reuters, European Commission.)
7. **UN talks set a 2-year path on killer robots** — states agree in Geneva to elaborate an instrument by 2028; whether it binds is undecided. (AP.)
8. **Jet lands safely after engine-fire alert** — Air Niugini PX19 diverts to Davao; all 146 aboard safe. (CAAP, AP.)
9. **Bitcoin sinks to $55,789** — down 9.9% at 05:56 UTC, lowest since September 2024, then back over $60,000 by evening. (CoinGecko, Investing.com.)
10. **Russell fastest in final Las Vegas practice** — 1:34.041 in the dry final session; Antonelli penalised 5 places, Verstappen on pole. (Formula 1.)
11. **Rahul hits a century against New Zealand** — 124 not out at tea, India 344 for 2, replying to 368; he finished on 136. (AFP, ICC.)
12. **Russian strikes kill 2 in Kryvyi Rih** — a boy of 7 and a paramedic die as missiles hit a restaurant, then rescuers; ~60 hurt. (AP.)
13. **BepiColombo reaches Mercury** — thrusters fire at 19:24 CET; ESA confirms orbit capture the same day, the second mission ever to orbit Mercury. (ESA.)

## Also on Saturday — 22 more stories

14. Basra power-station fire kills 4, 35 hurt. 15. Gaza drone strike kills 3 in food-aid van. 16. Iran says it downed a US MQ-9 drone over Hormuz. 17. Tehran: uranium stock stays in the country. 18. Paris: 82,500 march over living costs. 19. Taipei curbs short-selling after a -17.5% week. 20. Washington: Trump vows a 'tremendous' data-centre tax. 21. Beijing tells Japan to 'correct' Taiwan words. 22. Canberra: Australia and China agree AI talks. 23. Kyiv: Zelensky — Crimea bridge 'will not stay'. 24. Warsaw: Rutte — NATO will defend 'every inch'. 25. London: England beat All Blacks 37–12. 26. Bayelsa: at least 24 dead in boat capsize. 27. E. India: rain alerts as Akvan moves inland. 28. Lahore: Rizwan, Masood out of Pakistan contracts. 29. Dublin: Ireland beat South Africa 20–17. 30. Vancouver: defence rests in youth climate case. 31. Pyongyang: Kim tours factories after Trump trip. 32. Bangkok: six-point plan on arsenic in two rivers. 33. New Delhi: Pakistan minister joins SCO forum. 34. Sejong: freight train derails, none hurt. 35. Melbourne: Cummins keeps Australian captaincy.

## DATE CHECK — deliberately excluded (other days)

Left out as Friday 20 November's news: Poland missile · Kyiv bridges hit · Wall Street correction · Akvan landfall · UK–EU deal signed · Denmark expels Russian attaché · Jizan missiles (Fri eve). Older: ICJ Myanmar ruling (Thu 19 Nov) · Shenzhen summit. Not yet: COP31 final text (Sun 06:00 GMT) · Las Vegas GP race (Sun 04:00 UTC) · Liverpool v Man Utd (Sun).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG magic bytes, the 1024×1024 IHDR dimensions and the 1 MiB size limit. `draw_r3.py` (Python 3 + PIL) regenerates the image from scratch if you want to redraw it.

## Determinism

The program is deterministic: it copies fixed bytes, uses no network, no clock and no randomness, so repeated runs write byte-identical output. `draw_r3.py` is likewise deterministic — two runs produce a byte-identical `entry.png`.

<sub>Entered on [make.fun](https://make.fun/?ref=vfa7ye18&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
