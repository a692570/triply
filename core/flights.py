"""Flight search via fli MCP (Google Flights, no API key needed)."""
import subprocess, json


def search_flights(origin: str, destination: str, date: str, adults: int = 1) -> list:
    """Search flights. Returns list of flight dicts sorted by price."""
    try:
        result = subprocess.run(
            ["mcporter", "call", "fli.search_flights",
             f"origin={origin}", f"destination={destination}", f"departure_date={date}"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        flights = []
        for f in data.get("flights", []):
            legs = f["legs"]
            total_mins = sum(l["duration"] for l in legs)
            hrs, mins = divmod(total_mins, 60)
            stops = len(legs) - 1
            dep = legs[0]["departure_time"][11:16]
            arr = legs[-1]["arrival_time"][11:16]
            arr_day = "+1" if legs[-1]["arrival_time"][:10] > legs[0]["departure_time"][:10] else ""
            flights.append({
                "price": f["price"],
                "airline": legs[0]["airline"],
                "dep_time": dep,
                "arr_time": f"{arr}{arr_day}",
                "stops": stops,
                "duration": f"{hrs}h {mins}m",
                "duration_mins": total_mins,
            })
        return sorted(flights, key=lambda x: x["price"])[:8]
    except Exception as e:
        return []
