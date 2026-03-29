"""US State Dept travel advisory scraper. No API key needed."""
import urllib.request, re


def get_advisory(country: str) -> dict:
    """Fetch travel advisory for a country. Returns dict or None."""
    slug = country.lower().replace(" ", "-")
    url = f"https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/{slug}-travel-advisory.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        level = re.search(r"Level\s+(\d)\s*[-:]\s*([^<\n]{10,60})", html)
        updated = re.search(r"Last\s+Updated[:\s]+([A-Z][a-z]+ \d+, \d{4})", html)
        if level:
            lvl_num = level.group(1)
            return {
                "level": int(lvl_num),
                "text": level.group(2).strip(),
                "emoji": {"1": "🟢", "2": "🟡", "3": "🟠", "4": "🔴"}.get(lvl_num, "⚪"),
                "updated": updated.group(1) if updated else "unknown",
                "url": url,
            }
    except Exception:
        pass
    return None
