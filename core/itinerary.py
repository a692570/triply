"""Itinerary builder using Tavily for real destination-specific activities."""
import subprocess, json
from datetime import datetime, timedelta


def _search_activities(destination: str, prefs: str = "") -> list:
    """Search for real activities at destination via Tavily."""
    query = f"best things to do in {destination} how many hours each top attractions"
    if prefs:
        query += f" {prefs}"
    try:
        result = subprocess.run(
            ["mcporter", "call", "litellm.tavily_search",
             f"query={query}", "max_results:5"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        activities = []
        for r in data.get("results", []):
            content = r.get("content", "")
            # Extract activity-like sentences (lines with verbs + place names)
            lines = [l.strip() for l in content.split("\n") if len(l.strip()) > 20 and len(l.strip()) < 120]
            activities.extend(lines[:3])
        return activities[:15]
    except Exception:
        return []


def _parse_activities_to_slots(raw: list, destination: str, no_car: bool = False) -> list:
    """Convert raw activity text into structured slots with time estimates."""
    # Common duration patterns
    duration_hints = {
        "ruin": "2-3h", "temple": "2h", "museum": "2h", "cenote": "2h",
        "beach": "half day", "hike": "3h", "canyon": "3h", "park": "3h",
        "market": "1h", "tour": "4h", "reserve": "full day", "biosphere": "full day",
        "waterfall": "2h", "snorkel": "2h", "dive": "3h", "kayak": "2h",
        "old town": "2h", "historic": "2h", "fortress": "2h",
        "strip": "2h", "observation": "1h", "gondola": "1h",
        "food tour": "3h", "walking tour": "2h",
    }
    slots = []
    seen = set()
    for line in raw:
        # Skip generic/meta lines
        skip_words = ["click", "read more", "subscribe", "newsletter", "copyright", "cookie", "privacy", "http"]
        if any(w in line.lower() for w in skip_words):
            continue
        # Deduplicate similar activities
        key = line[:40].lower()
        if key in seen:
            continue
        seen.add(key)
        # Estimate duration
        duration = "2h"
        for keyword, dur in duration_hints.items():
            if keyword in line.lower():
                duration = dur
                break
        # Best time of day
        time_of_day = "Morning"
        if any(w in line.lower() for w in ["evening", "night", "sunset", "dinner", "bar", "club"]):
            time_of_day = "Evening"
        elif any(w in line.lower() for w in ["afternoon", "lunch", "midday"]):
            time_of_day = "Afternoon"
        elif any(w in line.lower() for w in ["morning", "sunrise", "early", "breakfast"]):
            time_of_day = "Morning"
        slots.append({
            "activity": line[:80],
            "duration": duration,
            "time_of_day": time_of_day,
            "notes": "no car: Uber/transit" if no_car and any(w in line.lower() for w in ["drive", "car", "road", "highway"]) else ""
        })
        if len(slots) >= 12:
            break
    return slots


def build_itinerary(destination: str, depart_date: str, return_date: str,
                    prefs: str = "", no_car: bool = False) -> list:
    """Build a real day-by-day itinerary using Tavily activity data."""
    start = datetime.strptime(depart_date, "%Y-%m-%d")
    end = datetime.strptime(return_date, "%Y-%m-%d")
    days = (end - start).days + 1

    # Get real activities from Tavily
    raw_activities = _search_activities(destination, prefs)
    activity_slots = _parse_activities_to_slots(raw_activities, destination, no_car)

    # Filter out casino/excluded activities based on prefs
    exclusions = [p.strip().lower().replace("no ", "") for p in prefs.split(",") if "no " in p.lower()]
    activity_slots = [a for a in activity_slots if not any(ex in a["activity"].lower() for ex in exclusions)]

    # Separate by time of day
    morning_acts = [a for a in activity_slots if a["time_of_day"] == "Morning"]
    afternoon_acts = [a for a in activity_slots if a["time_of_day"] == "Afternoon"]
    evening_acts = [a for a in activity_slots if a["time_of_day"] == "Evening"]

    # Fallback if Tavily returned nothing
    if not activity_slots:
        morning_acts = [{"activity": f"Explore {destination} highlights", "duration": "3h", "time_of_day": "Morning", "notes": ""}]
        afternoon_acts = [{"activity": "Local area exploration", "duration": "2h", "time_of_day": "Afternoon", "notes": ""}]
        evening_acts = [{"activity": "Dinner + evening walk", "duration": "2h", "time_of_day": "Evening", "notes": ""}]

    itinerary = []
    m_idx, a_idx, e_idx = 0, 0, 0

    for i in range(days):
        date = start + timedelta(days=i)
        date_str = date.strftime("%b %-d")
        is_arrival = i == 0
        is_departure = i == days - 1

        if is_arrival:
            activities = [
                {"time": "Afternoon", "activity": f"Check in, settle in {destination}", "duration": "1h", "notes": ""},
                {"time": "Evening", "activity": evening_acts[e_idx % len(evening_acts)]["activity"] if evening_acts else f"Evening walk around {destination}", "duration": "2h", "notes": "Light first day"},
            ]
            e_idx += 1
            theme = "Arrival"

        elif is_departure:
            activities = [
                {"time": "Morning", "activity": morning_acts[m_idx % len(morning_acts)]["activity"] if morning_acts else "Last morning stroll", "duration": "2h", "notes": ""},
                {"time": "Afternoon", "activity": "Head to airport", "duration": "", "notes": "Allow 2h before flight"},
            ]
            m_idx += 1
            theme = "Departure"

        else:
            # Full day: 1 morning + 1 afternoon + 1 evening activity
            acts = []
            if morning_acts:
                a = morning_acts[m_idx % len(morning_acts)]
                acts.append({"time": "Morning", "activity": a["activity"], "duration": a["duration"], "notes": a["notes"]})
                m_idx += 1
            if afternoon_acts:
                a = afternoon_acts[a_idx % len(afternoon_acts)]
                acts.append({"time": "Afternoon", "activity": a["activity"], "duration": a["duration"], "notes": a["notes"]})
                a_idx += 1
            elif morning_acts:
                a = morning_acts[m_idx % len(morning_acts)]
                acts.append({"time": "Afternoon", "activity": a["activity"], "duration": a["duration"], "notes": a["notes"]})
                m_idx += 1
            if evening_acts:
                a = evening_acts[e_idx % len(evening_acts)]
                acts.append({"time": "Evening", "activity": a["activity"], "duration": a["duration"], "notes": a["notes"]})
                e_idx += 1
            activities = acts if acts else [{"time": "All day", "activity": f"Explore {destination}", "duration": "full day", "notes": ""}]
            theme = f"Day {i} in {destination}"

        itinerary.append({
            "day_num": i + 1,
            "date": date_str,
            "theme": theme,
            "activities": activities,
        })

    return itinerary
