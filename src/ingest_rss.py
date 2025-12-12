import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import feedparser
from pathlib import Path

ECU = ZoneInfo("America/Guayaquil")
OUT = Path("output/raw_news.json")

SOURCES = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://www.dw.com/en/top-stories/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
]

def main():
    print(">>> Iniciando ingest_rss.py")

    items = []
    for url in SOURCES:
        d = feedparser.parse(url)
        source_name = d.feed.get("title", url)
        for e in d.entries[:30]:
            items.append({
                "title": e.get("title", "").strip(),
                "source": source_name,
                "url": e.get("link", ""),
                "published": e.get("published", ""),
                "snippet": (e.get("summary", "") or "")[:400].replace("\n", " ").strip()
            })

    payload = {
        "run_context": {
            "local_time_ecuador": datetime.now(timezone.utc)
            .astimezone(ECU)
            .strftime("%Y-%m-%d %H:%M"),
            "window_minutes": 1440,
            "language": "es-EC",
            "audience": "público general",
            "tone": "neutral, claro, profesional"
        },
        "items": items
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f">>> Noticias guardadas: {len(items)}")
    print(">>> Archivo raw_news.json generado")

if __name__ == "__main__":
    main()
