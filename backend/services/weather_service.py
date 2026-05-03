import aiohttp
from typing import Dict, List
from datetime import datetime

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    async def get_weather(self, latitude: float, longitude: float) -> Dict:
        """Get real-time weather for location using Open-Meteo API (Free, no key needed)"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,is_raining",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,rain_sum",
            "temperature_unit": "celsius",
            "timezone": "IST"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_weather(data)
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._default_weather()
    
    def _format_weather(self, data: Dict) -> Dict:
        """Convert raw weather data to pick-ranking format"""
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        return {
            "current": {
                "temperature": current.get("temperature_2m", 28),
                "is_raining": current.get("is_raining", False),
                "weather_code": current.get("weather_code", 0)
            },
            "forecast": {
                "next_7_days": list(zip(
                    daily.get("temperature_2m_max", []),
                    daily.get("temperature_2m_min", []),
                    daily.get("rain_sum", [])
                ))
            }
        }
    
    def _default_weather(self) -> Dict:
        return {
            "current": {
                "temperature": 28,
                "is_raining": False,
                "weather_code": 1
            },
            "forecast": {"next_7_days": []}
        }

weather_service = WeatherService()