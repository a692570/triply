# ✈️ triply

**Trip planning skill for Claude Code and OpenClaw.** Tell Claude where you want to go — it pulls live flight prices from multiple airports, digs up Reddit trip reports, finds hotels, checks weather and travel advisories, and builds a day-by-day itinerary. Outputs an HTML brief you can keep.

---

## Quickstart (Claude Code)

```bash
mkdir -p ~/.claude/skills/trip-planner
curl -o ~/.claude/skills/trip-planner/SKILL.md \
  https://raw.githubusercontent.com/a692570/triply/main/skill/SKILL.md
```

Then add your profile to `~/.claude/CLAUDE.md` once:

```
TRAVEL PROFILE:
- Home airports: SFO (also check OAK/SJC if cheaper)
- Budget style: mid-range, budget-conscious
- Dietary: needs vegetarian options on menu
- Skip: casinos as primary activity
```

Then just say: **"plan a trip to Cancun, April 14-19"**

---

## Quickstart (OpenClaw)

```bash
mkdir -p ~/clawd/agent-skills/skills/trip-planner
curl -o ~/clawd/agent-skills/skills/trip-planner/SKILL.md \
  https://raw.githubusercontent.com/a692570/triply/main/skill/SKILL.md
```

Add your profile to your OpenClaw workspace `USER.md` or memory.

---

## What it does

One conversation gives you:

- **Flights** — prices from all your home airports, flags cheaper alternatives
- **Reddit intel** — recent trip reports, neighborhood tips, what locals say to skip
- **Hotels** — 3 options (best value / mid-range / budget), location-aware
- **Weather** — conditions for your specific dates
- **Travel advisory** — US State Dept level, flagged if 3+
- **Itinerary** — day-by-day plan respecting your preferences and skip list
- **HTML report** — clean, linkable brief saved locally

---

## Why a skill vs a CLI

The CLI approach (see `triply.py`) scrapes approximated data from multiple sources.
The skill uses Claude's native research capabilities — actual web search, Reddit, real flight prices via browser — and gives opinionated recommendations instead of raw lists.

For non-technical friends: share this repo and the curl install above. Works with the free Claude.ai interface too if they add the skill content as a custom project instruction.

---

## HTML Report Design

The HTML output uses a flat sand/terracotta dark theme (no gradients):

- Background `#0f0d0b`, cards `#161310`
- Primary `#d97706` amber, accent `#c2603a` terracotta
- Sections: Flights, Hotels, Weather, Advisory, Activities, Restaurants, Itinerary timeline, Budget breakdown
- All booking links wired (Google Flights, OpenTable, State Dept)

See [`output/template.html`](output/template.html) for the template used by the Python CLI.

---

## Python CLI (alternative)

Prefer a one-shot command without a conversation:

```bash
# Setup
git clone https://github.com/a692570/triply
cd triply
pip install -r requirements.txt
cp .env.example .env  # only needed for Maps + Tavily

# Run
python triply.py --from SFO --to CUN \
  --depart 2026-04-14 --return 2026-04-19 \
  --adults 1 --prefs "outdoor activities, cenotes"
```

| Flag | Description | Default |
|---|---|---|
| `--from` | Origin city or IATA code | required |
| `--to` | Destination city or IATA code | required |
| `--depart` | Departure date (YYYY-MM-DD) | required |
| `--return` | Return date (YYYY-MM-DD) | required |
| `--adults` | Number of adults | 1 |
| `--no-car` | Plan around transit/Uber | false |
| `--prefs` | Preferences or exclusions | "" |
| `--budget` | Total budget in USD | none |
| `--html` | Export HTML report to path | none |

**API keys** (optional — core features work without them):
- `GOOGLE_MAPS_API_KEY` — ground transport directions ([get one](https://console.cloud.google.com/apis/credentials), free $200/mo credit)
- `TAVILY_API_KEY` — events + restaurants ([get one](https://app.tavily.com), free tier)

---

## Contributing

PRs welcome. Ideas:
- More flight data sources / scraping improvements
- Return flight timing logic
- Booking link integration
- Cached results for repeat queries
- Port to other AI platforms (Gemini CLI, etc.)

---

## License

MIT
