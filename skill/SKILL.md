---
name: trip-planner
description: Full trip planning with real research — flights from multiple airports, Reddit destination intel, hotels, weather, travel advisory, itinerary, and HTML brief. USE WHEN user says "plan a trip", "I want to go to X", "trip to X", "plan [destination]", or any travel planning request.
---

# Trip Planner

Plan any trip using real research — not hallucinated data. Pulls live flight prices, recent Reddit trip reports, hotel options, weather, and travel advisories, then builds a day-by-day itinerary and exports a clean HTML brief.

Works with **Claude Code**, **OpenClaw**, and any Claude environment with web access.

---

## First-Time Setup

Add your travel profile to your Claude memory or `CLAUDE.md` once. Never asked again.

```
TRAVEL PROFILE:
- Home airports: [your airport(s), e.g. SFO — list alternatives if willing to drive for cheaper flights]
- Budget style: [budget / mid-range / flexible / no cap]
- Dietary: [any restrictions, e.g. "needs vegetarian options on menu"]
- Skip: [things you don't want centered in itineraries, e.g. casinos, clubs]
- Travel style: [e.g. "pack a lot in" vs "slow travel", solo vs with partner]
```

---

## Activation

Say any of:
- "Plan a trip to [destination]"
- "I want to go to [X] in [month]"
- "Trip to [destination] [dates]"
- "Help me plan a trip"

---

## Step 1: Gather Parameters

Ask only what isn't provided. Don't re-ask anything in the travel profile.

**Required**: destination, dates or flexibility (e.g. "flexible in April", "April 14–19")
**Ask only if relevant**: solo or with someone (affects hotel count + budget), specific goals, hard budget cap

Once destination + dates are known, proceed immediately without further clarification.

---

## Step 2: Research (run in parallel)

### Flights
Search for prices from all listed home airports:
- "[origin] to [destination] flights [depart date]"
- "[destination] to [origin] flights [return date]"

Flag if alternative airports are >$50 cheaper. Capture: airline, price, duration, stops, times.
Check ±3 days if dates are flexible.

### Destination Intel (Reddit)
Run in parallel:
1. `site:reddit.com [destination] trip report 2025`
2. `site:reddit.com [destination] travel tips first time`
3. `site:reddit.com [destination] best neighborhood stay`
4. `[destination] [dietary restriction] food restaurants`

Extract: neighborhoods to base in, must-do activities, what locals say to skip.

### Hotels
- "best value hotels [destination] [best neighborhood from above]"
- Return 3 options: best value / mid-range pick / budget fallback
- Note proximity to main attractions

### Weather
Fetch: `https://wttr.in/[destination]?format=j1`
Parse temp range, rain chance, conditions for travel dates. Flag if weather is a concern.

### Travel Advisory
Fetch: `https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/[country]-travel-advisory.html`
Note level 1–4. Level 3–4: flag prominently at top of output.

### Activities + Food
1. "top things to do [destination] [travel month]"
2. "best restaurants [destination] [dietary preference] friendly"
3. "events [destination] [travel month year]"

Filter itinerary to exclude activities flagged in user's skip list.

---

## Step 3: Build Itinerary

- **Day 1**: Arrival + one easy nearby activity + dinner at a recommended spot
- **Middle days**: Max 2–3 activities per day, mix active + relaxed
- **Last day**: Morning activity + 2hr departure buffer minimum
- **Evenings**: Rotate restaurant picks, note dietary-friendly options
- **Skip-list items**: Include at most once if culturally relevant, never as a day anchor

---

## Step 4: Output

### In-chat summary (lead with this)
Keep it to 6–8 lines:
- Best flight option + price (flag cheaper alternatives)
- One hotel recommendation + why
- 3 non-negotiable activities
- One watch-out (advisory level, weather, peak season, etc.)
- Rough total budget estimate

### HTML Report
Generate a full HTML report saved to `~/.claude/output/html/trip-[destination]-[depart-date].html`

Design system (flat, no gradients):
- Background `#0f0d0b`, card bg `#161310`, border `rgba(255,255,255,0.07)`
- Primary `#d97706` (amber), accent `#c2603a` (terracotta), muted `#7a6f67`
- Font: Inter (Google Fonts)
- Sections: Flights table, Hotels, Weather, Advisory banner, Events, Restaurants, Itinerary timeline, Budget breakdown with stacked bar
- All links wired: Google Flights booking URLs, OpenTable for restaurants, State Dept for advisory

Tell the user the output path when done.

### Opinionated recommendation
Give a clear call, not just options:
- "Book the [airline] nonstop — [reason] vs [alternative]"
- "Stay in [neighborhood] — [reason], avoid [other area]"
- "Skip [overhyped attraction] per recent trip reports, do [alternative] instead"

---

## Install

### Claude Code
```bash
mkdir -p ~/.claude/skills/trip-planner
curl -o ~/.claude/skills/trip-planner/SKILL.md \
  https://raw.githubusercontent.com/a692570/triply/main/skill/SKILL.md
```

### OpenClaw
```bash
mkdir -p ~/clawd/agent-skills/skills/trip-planner
curl -o ~/clawd/agent-skills/skills/trip-planner/SKILL.md \
  https://raw.githubusercontent.com/a692570/triply/main/skill/SKILL.md
```

Then add your travel profile to memory or `CLAUDE.md` as described in First-Time Setup.

---

## CLI (Alternative)

Prefer a one-shot command instead of a conversation? See the Python CLI in the repo root:
```bash
python triply.py --from SFO --to CUN --depart 2026-04-14 --return 2026-04-19 --adults 1
```
