"""Weather via wttr.in. No API key needed."""
import subprocess


def get_weather(city: str) -> str:
    """Get weather summary for a city."""
    try:
        result = subprocess.run(
            ["curl", "-s", f"wttr.in/{city.replace(' ', '+')}?format=%l:+%C,+%t+(feels+%f),+humidity+%h", "-A", "curl"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return "Weather unavailable"
