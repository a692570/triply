#!/usr/bin/env python3
"""triply — AI-powered travel brief generator."""
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

from core.flights import search_flights
from core.hotels import search_hotels
from core.transport import get_transport
from core.advisory import get_advisory
from core.events import get_events
from core.weather import get_weather
from core.itinerary import build_itinerary
from output.report import render_terminal, render_html


def main():
    parser = argparse.ArgumentParser(
        prog="triply",
        description="AI-powered travel brief: flights, hotels, transport, itinerary in one command."
    )
    parser.add_argument("--from", dest="origin", required=True, help="Origin city or IATA code (e.g. SFO)")
    parser.add_argument("--to", dest="destination", required=True, help="Destination city or IATA code (e.g. LAS)")
    parser.add_argument("--depart", required=True, help="Departure date YYYY-MM-DD")
    parser.add_argument("--return", dest="return_date", required=True, help="Return date YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=1, help="Number of adults (default: 1)")
    parser.add_argument("--html", dest="html_output", default=None, help="Export HTML report to this path")
    parser.add_argument("--no-car", action="store_true", help="No rental car — plan around transit/Uber")
    parser.add_argument("--prefs", default="", help='Preferences e.g. "no casino, outdoor activities"')
    parser.add_argument("--budget", type=float, default=None, help="Total budget in USD")
    args = parser.parse_args()

    print(f"\n✈️  triply — planning your trip to {args.destination}...\n")

    print("  Searching flights...")
    outbound = search_flights(args.origin, args.destination, args.depart, args.adults)
    inbound = search_flights(args.destination, args.origin, args.return_date, args.adults)

    print("  Searching hotels...")
    hotels = search_hotels(args.destination, args.depart, args.return_date, args.adults)

    print("  Getting ground transport...")
    transport = get_transport(f"{args.destination} Airport", args.destination)

    print("  Checking weather...")
    weather = get_weather(args.destination)

    print("  Fetching travel advisory...")
    # Derive country from destination (simple heuristic)
    advisory = None
    if args.destination.upper() not in ["SFO", "LAX", "JFK", "LAS", "EWR", "ORD", "ATL", "DFW", "SEA", "BOS"]:
        advisory = get_advisory(args.destination)

    print("  Finding events + restaurants...")
    events_data = get_events(args.destination, args.depart, args.return_date)

    print("  Building itinerary...")
    itinerary = build_itinerary(
        args.destination, args.depart, args.return_date,
        prefs=args.prefs, no_car=args.no_car
    )

    # Budget rollup
    from datetime import datetime
    nights = (datetime.strptime(args.return_date, "%Y-%m-%d") - datetime.strptime(args.depart, "%Y-%m-%d")).days
    flight_cost = (outbound[0]["price"] + inbound[0]["price"]) * args.adults if outbound and inbound else 0
    hotel_cost = hotels[0]["price_per_night"] * nights * (1 if args.adults <= 2 else 2) if hotels else 0
    transport_est = 40
    budget_data = {
        "flights": flight_cost,
        "hotel": hotel_cost,
        "hotel_details": f"${hotels[0]['price_per_night']}/night x {nights} nights" if hotels else "",
        "transport": transport_est,
        "total": flight_cost + hotel_cost + transport_est,
        "budget": args.budget,
    }

    trip = {
        "origin": args.origin,
        "destination": args.destination,
        "depart_date": args.depart,
        "return_date": args.return_date,
        "adults": args.adults,
        "prefs": args.prefs,
        "no_car": args.no_car,
    }

    data = {
        "trip": trip,
        "outbound_flights": outbound,
        "inbound_flights": inbound,
        "hotels": hotels,
        "transport": transport,
        "weather": weather,
        "advisory": advisory,
        "events": events_data.get("events", []),
        "restaurants": events_data.get("restaurants", []),
        "itinerary": itinerary,
        "budget": budget_data,
    }

    render_terminal(data)

    if args.html_output:
        render_html(data, args.html_output)
        print(f"\n📄 HTML report saved to: {args.html_output}\n")


if __name__ == "__main__":
    main()
