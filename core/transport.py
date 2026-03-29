"""Ground transport via Google Maps Directions API."""
import os, re
try:
    import googlemaps
    HAS_GOOGLEMAPS = True
except ImportError:
    HAS_GOOGLEMAPS = False

from datetime import datetime


def get_transport(origin: str, destination: str) -> dict:
    """Get transit + driving directions. Returns dict or None if no key."""
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key or not HAS_GOOGLEMAPS:
        return None
    try:
        gmaps = googlemaps.Client(key=key)
        out = {}
        for mode in ["transit", "driving"]:
            r = gmaps.directions(origin, destination, mode=mode, departure_time=datetime.now())
            if r:
                leg = r[0]["legs"][0]
                steps = [re.sub("<[^>]+>", "", s["html_instructions"])[:70] for s in leg["steps"][:5]]
                out[mode] = {
                    "duration": leg["duration"]["text"],
                    "distance": leg["distance"]["text"],
                    "steps": steps,
                }
        return out if out else None
    except Exception:
        return None
