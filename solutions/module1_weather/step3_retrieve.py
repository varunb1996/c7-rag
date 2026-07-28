"""Step 3 — SOLUTION. Metadata filtering: the retrieval tool itself."""
import json
from collections import defaultdict

INDEX = json.load(open("index.json"))


def get_weather_history(city, start_date, end_date, month=None):
    """Daily summaries for a city between two dates.

    Pass month (1-12) to keep only that month across the range,
    e.g. every August of the last ten years.
    """
    y0, y1 = int(start_date[:4]), int(end_date[:4])

    hits = [
        e
        for e in INDEX
        if e["city"].lower() == city.lower() and y0 <= e["year"] <= y1
    ]  # the metadata filter

    days = defaultdict(lambda: {"rain_mm": 0.0, "t_max": None})
    for entry in hits:  # only matching chunks are ever opened
        hours = json.load(open(entry["path"]))["hourly"]
        for ts, temp, rain in zip(
            hours["time"], hours["temperature_2m"], hours["precipitation"]
        ):
            day = ts[:10]
            if day < start_date or day > end_date:
                continue
            if month and int(day[5:7]) != month:
                continue
            d = days[day]
            d["rain_mm"] = round(d["rain_mm"] + (rain or 0.0), 1)
            d["t_max"] = temp if d["t_max"] is None else max(d["t_max"], temp)
    return [{"date": k, **v} for k, v in sorted(days.items())]


if __name__ == "__main__":
    result = get_weather_history("Bengaluru", "2016-01-01", "2025-12-31", month=8)
    payload = json.dumps(result)

    import tiktoken

    enc = tiktoken.get_encoding("cl100k_base")
    print(f"{len(result)} daily summaries, ~{len(enc.encode(payload)):,} tokens")
    print("first:", result[0])
    print("last: ", result[-1])
