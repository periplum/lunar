<table align="center">
<tr><td align="center" width="640">

## ▶&nbsp; [Open the interactive map](https://periplum.github.io/lunar/)

🌙 &nbsp;Every soft landing on the Moon since 1959, on a lunar basemap

</td></tr>
</table>

# lunar

[![Built with Periplum](https://img.shields.io/badge/built_with-Periplum-4da3ff)](https://periplum.js.org)

Crewed and robotic soft landings (plus notable crashes) plotted by selenographic
coordinates. Gold = crewed, blue = robotic, red = failed. Press play to watch the landing
sequence, or drag the date slider.

## Data & updates

`data.json` is **hand-curated** — it carries clean crewed/robotic/failed status and tidy
notes that no single API provides.

[`source.py`](source.py) is a discovery aid: it queries **Wikidata** for objects located on
the Moon globe with a landing date (Python standard library only, no dependencies):

```sh
python source.py > wikidata-candidates.json
```

### GitHub Actions

[`.github/workflows/refresh-data.yml`](.github/workflows/refresh-data.yml) runs `source.py`
**twice a year** (and on manual *Run workflow*) and uploads the result as a build
**artifact**. The periplum org blocks Actions from pushing or opening PRs, so the flow is:
download the artifact → fold any new landings into the curated `data.json` → commit.

---

Built with [Periplum](https://periplum.js.org) · [periplum.js.org](https://periplum.js.org)
