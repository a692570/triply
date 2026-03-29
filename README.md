# ✈️ triply

AI-powered travel brief generator. One command gives you flights, hotels, ground transport, weather, travel advisory, local events, restaurant picks, and a day-by-day itinerary — all pulled from live data.

```
$ python triply.py --from SFO --to LAS --depart 2026-06-05 --return 2026-06-07 --adults 2 --no-car --prefs "no casino"
```

![triply terminal output](https://github.com/a692570/triply/raw/main/examples/screenshot-placeholder.png)

---

## What it does

triply pulls from multiple free data sources and assembles a complete trip brief in seconds:

| Section | Source | API Key? |
|---|---|---|
| ✈️ Flights | Google Flights (via fli) | None |
| 🏨 Hotels | Google Hotels (via fast-hotels) | None |
| 🚗 Ground transport | Google Maps Directions | Free ($200/mo credit) |
| 🌤️ Weather | wttr.in | None |
| 🛡️ Travel advisory | US State Dept | None |
| 🎟️ Events | Tavily Search | Free tier |
| 🍽️ Restaurants | Tavily Search | Free tier |
| 📍 Itinerary | Generated | None |

---

## Prerequisites

- Python 3.10+
- [fli](https://github.com/punitarani/fli): `pipx install flights`
- [mcporter](https://github.com/openclaw/mcporter): for fli MCP + Tavily search

---

## Setup

```bash
# Clone
git clone https://github.com/a692570/triply
cd triply

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your API keys (see .env.example for instructions)
```

---

## Usage

```bash
# Weekend trip, no car
python triply.py --from SFO --to LAS --depart 2026-06-05 --return 2026-06-07 --adults 2 --no-car

# Week-long trip with preferences
python triply.py --from SFO --to CUN --depart 2026-06-15 --return 2026-06-22 --adults 3 --prefs "outdoor activities, no resort fees"

# Export HTML report
python triply.py --from JFK --to LHR --depart 2026-07-10 --return 2026-07-17 --adults 1 --html london-trip.html

# With budget
python triply.py --from SFO --to NRT --depart 2026-08-01 --return 2026-08-10 --adults 2 --budget 3000
```

---

## API Keys

**Google Maps** (for ground transport):
1. Go to [console.cloud.google.com](https://console.cloud.google.com/apis/credentials)
2. Create an API key
3. Enable: Directions API, Geocoding API
4. Add to `.env` as `GOOGLE_MAPS_API_KEY`
5. Free $200/month credit — more than enough for personal use

**Tavily** (for events + restaurant discovery):
1. Sign up at [app.tavily.com](https://app.tavily.com)
2. Copy your API key
3. Add to `.env` as `TAVILY_API_KEY`
4. Free tier: 1000 searches/month

Both are optional — triply works without them, you just won't get transport directions or events.

---

## Contributing

PRs welcome. Especially interested in:
- Better itinerary generation (destination-specific activities)
- Return flight timing logic improvements
- More hotel data sources
- Booking link integration

---

## License

MIT
