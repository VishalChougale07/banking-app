import aiohttp
from typing import List, Dict
from config import settings

class GooglePlacesService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place"
    
    async def search_restaurants(self, query: str, location: str, latitude: float = None, longitude: float = None) -> List[Dict]:
        """Search restaurants near location using Google Places API"""
        params = {
            "query": f"{query} restaurants in {location}",
            "key": settings.GOOGLE_PLACES_API_KEY,
            "fields": "formatted_address,name,rating,user_ratings_total,opening_hours,photos,place_id"
        }
        
        if latitude and longitude:
            params["location"] = f"{latitude},{longitude}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.BASE_URL}/textsearch/json", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_restaurants(data.get("results", []))
        except Exception as e:
            print(f"Google Places API error: {e}")
            return []
    
    async def get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a place"""
        params = {
            "place_id": place_id,
            "key": settings.GOOGLE_PLACES_API_KEY,
            "fields": "name,rating,user_ratings_total,formatted_address,opening_hours,photos,formatted_phone_number,website,business_status"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.BASE_URL}/details/json", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("result", {})
        except Exception as e:
            print(f"Google Places details error: {e}")
            return {}
    
    def _format_restaurants(self, results: List) -> List[Dict]:
        """Format restaurant data for discovery feed"""
        formatted = []
        for place in results[:10]:  # Top 10 results
            formatted.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating", 4.0),
                "review_count": place.get("user_ratings_total", 0),
                "place_id": place.get("place_id"),
                "photo_url": self._get_photo_url(place.get("photos", [])),
                "is_open": self._check_open_status(place.get("opening_hours", {}))
            })
        return formatted
    
    def _get_photo_url(self, photos: List) -> str:
        """Extract photo URL from Google Places response"""
        if photos:
            photo_ref = photos[0].get("photo_reference")
            return f"{self.BASE_URL}/photo?maxwidth=400&photo_reference={photo_ref}&key={settings.GOOGLE_PLACES_API_KEY}"
        return "https://via.placeholder.com/400x300?text=Restaurant"
    
    def _check_open_status(self, opening_hours: Dict) -> bool:
        """Check if place is currently open"""
        return opening_hours.get("open_now", True)

google_places_service = GooglePlacesService()