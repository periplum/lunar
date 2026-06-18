#!/usr/bin/env python3
"""Refresh lunar-landing data from Wikidata (the proper, evolving source).

`data.json` is hand-curated and authoritative for display (it carries clean
crewed/robotic/failed status and tidy notes). This script queries Wikidata for
objects with a coordinate location *on the Moon* and a landing date, and prints
them as Periplum canonical items — use it to spot new landings to add, or to
regenerate the dataset.

    python source.py            # print canonical JSON to stdout
    python source.py > new.json # capture it

Wikidata is queried via its public SPARQL endpoint; no key required.
"""

import json
import sys
import urllib.parse
import urllib.request

SPARQL = "https://query.wikidata.org/sparql"

# Objects whose coordinate location uses the Moon globe (wd:Q405), with a
# spacecraft-landing date (P619) or point-in-time (P585). Crew (P1029) => crewed.
QUERY = """
SELECT ?item ?itemLabel ?lat ?lon ?date (COUNT(?crew) AS ?crewCount) WHERE {
  ?item p:P625 ?coordStmt .
  ?coordStmt psv:P625 ?coordNode .
  ?coordNode wikibase:geoGlobe wd:Q405 ;
             wikibase:geoLatitude ?lat ;
             wikibase:geoLongitude ?lon .
  OPTIONAL { ?item wdt:P619 ?date . }
  OPTIONAL { ?item wdt:P585 ?date2 . }
  OPTIONAL { ?item wdt:P1029 ?crew . }
  BIND(COALESCE(?date, ?date2) AS ?date)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?item ?itemLabel ?lat ?lon ?date
ORDER BY ?date
"""


def fetch():
    url = SPARQL + "?" + urllib.parse.urlencode({"query": QUERY, "format": "json"})
    req = urllib.request.Request(url, headers={
        "User-Agent": "PeriplumLunar/1.0 (https://github.com/periplum/lunar)",
        "Accept": "application/sparql-results+json",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def to_items(raw):
    items = []
    for b in raw.get("results", {}).get("bindings", []):
        try:
            lat = round(float(b["lat"]["value"]), 3)
            lon = round(float(b["lon"]["value"]), 3)
        except (KeyError, ValueError):
            continue
        name = b.get("itemLabel", {}).get("value") or b.get("item", {}).get("value", "")
        date = (b.get("date", {}).get("value") or "")[:10] or None
        crewed = int(b.get("crewCount", {}).get("value", "0")) > 0
        items.append({
            "name": name, "date": date, "status": "crewed" if crewed else "robotic",
            "placements": [{"map": "moon", "lat": lat, "lon": lon, "label": name,
                            "popup": {"Source": "Wikidata"}}],
        })
    return items


def main():
    items = to_items(fetch())
    print(f"# fetched {len(items)} lunar-surface objects from Wikidata", file=sys.stderr)
    json.dump({"items": items}, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
