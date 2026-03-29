"""Itinerary builder."""
from datetime import datetime, timedelta


def build_itinerary(destination: str, depart_date: str, return_date: str,
                    prefs: str = "", no_car: bool = False) -> list:
    """Build day-by-day itinerary. Returns list of day dicts."""
    start = datetime.strptime(depart_date, "%Y-%m-%d")
    end = datetime.strptime(return_date, "%Y-%m-%d")
    days = (end - start).days + 1
    itinerary = []

    no_casino = "casino" in prefs.lower() or "no casino" in prefs.lower()
    transport_note = "Uber/transit" if no_car else "car/Uber"

    for i in range(days):
        date = start + timedelta(days=i)
        date_str = date.strftime("%b %-d")
        is_arrival = i == 0
        is_departure = i == days - 1

        if is_arrival:
            activities = [
                {"time": "Afternoon", "activity": "Check in, settle", "duration": "1h", "notes": ""},
                {"time": "Evening", "activity": f"Explore nearby area of {destination}", "duration": "2h", "notes": "Light first day"},
            ]
            theme = "Arrival"
        elif is_departure:
            activities = [
                {"time": "Morning", "activity": "Breakfast + last walk", "duration": "2h", "notes": ""},
                {"time": "Afternoon", "activity": f"{transport_note} to airport", "duration": "", "notes": "Allow 2h before flight"},
            ]
            theme = "Departure"
        else:
            # Full day
            activities = [
                {"time": "Morning", "activity": f"Top attraction in {destination}", "duration": "2-3h", "notes": "Go early for fewer crowds"},
                {"time": "Afternoon", "activity": "Second activity or leisure", "duration": "2h", "notes": ""},
                {"time": "Evening", "activity": "Dinner + nightlife", "duration": "2h", "notes": ""},
            ]
            theme = f"Day {i} — Explore"

        itinerary.append({
            "day_num": i + 1,
            "date": date_str,
            "theme": theme,
            "activities": activities,
        })

    return itinerary
