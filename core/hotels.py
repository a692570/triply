"""Hotel search via fast-hotels (Google Hotels, no API key needed)."""
try:
    from fast_hotels.hotels_impl import HotelData, Guests
    from fast_hotels import get_hotels as _get_hotels
    HAS_FAST_HOTELS = True
except ImportError:
    HAS_FAST_HOTELS = False


def search_hotels(location: str, checkin: str, checkout: str, adults: int = 1) -> list:
    """Search hotels. Returns list sorted by rating."""
    if not HAS_FAST_HOTELS:
        return []
    try:
        import warnings
        warnings.filterwarnings("ignore")
        result = _get_hotels(
            hotel_data=[HotelData(checkin_date=checkin, checkout_date=checkout, location=location)],
            guests=Guests(adults=adults, children=0, infants=0),
            limit=8,
            sort_by="rating",
            fetch_mode="fallback",
        )
        return [
            {
                "price_per_night": h.price,
                "rating": h.rating,
                "name": h.name,
                "url": getattr(h, "url", ""),
            }
            for h in result.hotels
            if h.rating
        ]
    except Exception:
        return []
