
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/google_maps_mcp')))

import pytest
from services.places import PlacesService

class MockGMaps:
    def geocode(self, location):
        if location == "Nowhere":
            return []
        return [{"geometry": {"location": {"lat": 12.34, "lng": 56.78}}}]

    def places_nearby(self, location, radius, type):
        return {"results": [
            {"name": "Test Place", "rating": 4.5, "vicinity": "123 Test St", "place_id": "abc123", "types": [type], "user_ratings_total": 100},
            {"name": "Another Place", "rating": 3.0, "vicinity": "456 Test Ave", "place_id": "def456", "types": [type], "user_ratings_total": 50}
        ]}

def test_get_places_nearby():
    service = PlacesService(MockGMaps())
    results = service.get_places_nearby("Somewhere", "restaurant")
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["name"] == "Test Place"

def test_get_places_nearby_no_results():
    service = PlacesService(MockGMaps())
    results = service.get_places_nearby("Nowhere", "restaurant")
    assert results == []

def test_get_places_nearby_sort_by_rating():
    service = PlacesService(MockGMaps())
    results = service.get_places_nearby("Somewhere", "restaurant", rank_by="rating")
    assert results[0]["rating"] >= results[1]["rating"]
