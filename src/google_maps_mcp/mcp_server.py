
"""
Entrypoint for Google Maps MCP server using MCP library.
"""

# MCP imports
from mcp.server.fastmcp import FastMCP

import os
import googlemaps
import logging
from .services.places import PlacesService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger("google_maps_mcp.mcp_server")

# Set up Google Maps client and inject into PlacesService
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if not api_key:
    logger.warning("GOOGLE_MAPS_API_KEY not set!")
    
gmaps_client = googlemaps.Client(key=api_key) if api_key else None
places_service = PlacesService(gmaps_client)
mcp = FastMCP("GoogleMapsMCP", version="1.0.0")

# Register tools
@mcp.tool()
def find_places_nearby(name: str, arguments: dict) -> list:
    """
    Find places of a given type near a location (or 'me'), within 5km, sorted by rating or distance.
    arguments: {"location": str, "place_type": str, "sort_by": "rating"|"distance"}
    """
    location = arguments.get("location", "Bangalore")
    place_type = arguments.get("place_type", "restaurant")
    sort_by = arguments.get("sort_by", "rating")
    logger.info(f"find_places_nearby called with location='{location}', place_type='{place_type}', sort_by='{sort_by}'")
    # If location is 'me', you would use user's coordinates (not implemented here)
    results = places_service.get_places_nearby(location, place_type, radius=5000, rank_by=sort_by)
    logger.info(f"Found {len(results)} places for location='{location}', type='{place_type}'")
    return [
        {
            "name": p.get("name"),
            "rating": p.get("rating"),
            "vicinity": p.get("vicinity"),
            "place_id": p.get("place_id"),
            "types": p.get("types"),
            "user_ratings_total": p.get("user_ratings_total")
        }
        for p in results
    ]

def main():
    logger.info("Starting Google Maps MCP server...")
    mcp.run()