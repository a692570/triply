"""Events + restaurant discovery via Tavily (through mcporter)."""
import subprocess, json


def _tavily(query: str, max_results: int = 5) -> list:
    try:
        result = subprocess.run(
            ["mcporter", "call", "litellm.tavily_search",
             f"query={query}", f"max_results:{max_results}"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        return [{"title": r["title"], "snippet": r["content"][:200]} for r in data.get("results", [])]
    except Exception:
        return []


def get_events(destination: str, depart_date: str, return_date: str) -> dict:
    """Get events + restaurant recommendations for a destination."""
    from datetime import datetime
    month = datetime.strptime(depart_date, "%Y-%m-%d").strftime("%B %Y")
    events = _tavily(f"events concerts festivals {destination} {month}")
    restaurants = _tavily(f"best restaurants {destination} 2026 worth booking reservation required")
    return {"events": events, "restaurants": restaurants}
