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
mcp = FastMCP(
    "GoogleMapsMCP",
    version="1.0.0",
    description="A Model Context Protocol (MCP) server for querying Google Maps and Places API for places, restaurants, tourist attractions, and more. Provides tools to find places near a location, sorted by rating or distance."
)

# Register tools
@mcp.tool()
def find_places_nearby(location: str, place_type: str = "places_of_interest", sort_by: str = "rating") -> list:
    """
    Find places near a given location using Google Maps Places API.

    Args:
        location (str): Address or area name to search near. Required.
        place_type (str, optional): Google Places type (e.g., 'restaurant', 'tourist_attraction', 'meal_takeaway'). Default is 'places_of_interest'.
        sort_by (str, optional): Sort results by 'rating' or 'distance'. Default is 'rating'.

    Returns:
        list: List of places, each as a dict with keys: name, rating, vicinity, place_id, types, user_ratings_total.

    Example:
        find_places_nearby(location='New York', place_type='restaurant', sort_by='distance')
    """
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