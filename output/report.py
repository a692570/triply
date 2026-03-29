"""Terminal (rich) and HTML report rendering."""
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

console = Console()


def render_terminal(data: dict):
    trip = data["trip"]
    console.print(f"\n[bold cyan]🗺️  TRIP BRIEF — {trip['origin']} → {trip['destination']}[/]")
    console.print(f"[dim]{trip['depart_date']} to {trip['return_date']} · {trip['adults']} adult(s)[/]\n")

    # Flights
    for label, flights in [("✈️  OUTBOUND", data["outbound_flights"]), ("✈️  RETURN", data["inbound_flights"])]:
        if flights:
            t = Table(box=box.SIMPLE_HEAD, show_header=True)
            t.add_column("Price", style="green bold")
            t.add_column("Airline")
            t.add_column("Dep")
            t.add_column("Arr")
            t.add_column("Stops")
            t.add_column("Duration")
            for f in flights[:6]:
                stops = "nonstop" if f["stops"] == 0 else f"{f['stops']} stop"
                t.add_row(f"${f['price']}", f["airline"], f["dep_time"], f["arr_time"], stops, f["duration"])
            console.print(Panel(t, title=label, border_style="blue"))

    # Hotels
    if data["hotels"]:
        t = Table(box=box.SIMPLE_HEAD)
        t.add_column("Price/night", style="green bold")
        t.add_column("Rating")
        t.add_column("Hotel")
        for h in data["hotels"][:6]:
            t.add_row(f"${h['price_per_night']}", f"{h['rating']}★" if h['rating'] else "N/A", h["name"])
        console.print(Panel(t, title="🏨  HOTELS", border_style="blue"))

    # Transport
    if data["transport"]:
        lines = []
        for mode, info in data["transport"].items():
            lines.append(f"[bold]{mode.upper()}:[/] {info['duration']} | {info['distance']}")
        console.print(Panel("\n".join(lines), title="🚗  GROUND TRANSPORT", border_style="blue"))

    # Weather
    if data["weather"]:
        console.print(Panel(data["weather"], title="🌤️  WEATHER", border_style="blue"))

    # Advisory
    if data["advisory"]:
        a = data["advisory"]
        console.print(Panel(f"{a['emoji']} Level {a['level']}: {a['text']} (updated {a['updated']})",
                            title="🛡️  TRAVEL ADVISORY", border_style="yellow"))

    # Events
    if data["events"]:
        lines = [f"• {e['title']}" for e in data["events"][:5]]
        console.print(Panel("\n".join(lines), title="🎟️  EVENTS", border_style="blue"))

    # Restaurants
    if data["restaurants"]:
        lines = [f"• {r['title']}" for r in data["restaurants"][:4]]
        console.print(Panel("\n".join(lines), title="🍽️  RESTAURANTS", border_style="blue"))

    # Itinerary
    if data["itinerary"]:
        lines = []
        for day in data["itinerary"]:
            lines.append(f"[bold cyan]Day {day['day_num']} ({day['date']}) — {day['theme']}[/]")
            for act in day["activities"]:
                note = f" — {act['notes']}" if act["notes"] else ""
                dur = f" (~{act['duration']})" if act["duration"] else ""
                lines.append(f"  [dim]{act['time']}:[/] {act['activity']}{dur}{note}")
            lines.append("")
        console.print(Panel("\n".join(lines), title="📍  ITINERARY", border_style="blue"))

    # Budget
    b = data["budget"]
    t = Table(box=box.SIMPLE_HEAD)
    t.add_column("Item")
    t.add_column("Cost", style="green")
    t.add_row("Flights", f"${b['flights']:.0f}")
    t.add_row(f"Hotel ({b['hotel_details']})", f"${b['hotel']:.0f}")
    t.add_row("Transport (est.)", f"${b['transport']:.0f}")
    t.add_row("[bold]Total[/]", f"[bold green]${b['total']:.0f}[/]")
    if b["budget"]:
        t.add_row("Your budget", f"${b['budget']:.0f}")
    console.print(Panel(t, title="💰  BUDGET", border_style="green"))


def render_html(data: dict, output_path: str):
    try:
        from jinja2 import Environment, FileSystemLoader
        from datetime import datetime
        template_dir = os.path.join(os.path.dirname(__file__))
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("template.html")
        html = template.render(**data, generated_at=datetime.now().strftime("%B %d, %Y at %H:%M"))
        with open(output_path, "w") as f:
            f.write(html)
    except Exception as e:
        console.print(f"[red]HTML export failed: {e}[/]")
