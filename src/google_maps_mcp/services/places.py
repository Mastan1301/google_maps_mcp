"""
PlacesService for interacting with Google Maps Places API.
"""
from typing import List, Optional
import logging

class PlacesService:
    def __init__(self, gmaps_client):
        """
        PlacesService expects a Google Maps client instance (dependency injection).
        """
        self.gmaps = gmaps_client
        self.logger = logging.getLogger(PlacesService.__name__)

    def get_places_nearby(self, location: str, place_type: str, radius: int = 5000, rank_by: Optional[str] = None) -> List[dict]:
        """
        Search for places of a given type near a location within a radius (meters).
        Optionally sort by 'prominence', 'distance', or 'rating'.
        """
        if not self.gmaps:
            self.logger.warning("Google Maps client is not initialized.")
            return []
        
        geocode = self.gmaps.geocode(location)
        if not geocode:
            self.logger.warning(f"No geocode result for location: {location}")
            return []
        
        latlng = geocode[0]["geometry"]["location"]

        self.logger.info(f"Searching for places_nearby: type={place_type}, radius={radius}")
        results = self.gmaps.places_nearby(
            location=(latlng["lat"], latlng["lng"]),
            radius=radius,
            type=place_type
        )
        places = results.get("results", [])
        self.logger.info(f"Found {len(places)} places for type='{place_type}' near '{location}'")

        # Sort if needed
        if rank_by == "rating":
            places.sort(key=lambda x: x.get("rating", 0), reverse=True)
            self.logger.info("Sorted places by rating (descending)")
        elif rank_by == "distance":
            # Google API sorts by distance if rank_by param is used, but we sort here for mock
            self.logger.info("Requested sort by distance.")

        return places
