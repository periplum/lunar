# lunar — soft landings on the Moon

[![Built with Periplum](https://img.shields.io/badge/built_with-Periplum-4da3ff)](https://periplum.js.org)

Every crewed and robotic soft landing on the Moon (plus a few notable crashes) since 1959,
plotted by **selenographic coordinates** on a lunar basemap — a different *world*, same
Periplum engine.

**[▶ Open the map](https://periplum.github.io/lunar/)** — press play to watch the landing
sequence unfold, or drag the date slider.

Gold = crewed (Apollo) · blue = robotic · red = failed/crashed.

## Data

`data.json` is hand-curated (clean status + notes). It can be refreshed/augmented from the
**proper evolving source — [Wikidata](https://www.wikidata.org)** — via
[`source.py`](source.py), which queries objects with a coordinate location on the Moon
(globe `wd:Q405`) and a landing date:

```sh
python source.py > candidates.json   # see what Wikidata knows; add new landings
```

A lunar mission lands only a few times a year, so a refresh workflow would run at most
twice a year.

## Credits

A showcase consumer of **[Periplum](https://github.com/periplum/periplum)**.
Moon basemap texture © [Solar System Scope](https://www.solarsystemscope.com/textures/)
(CC BY 4.0).
