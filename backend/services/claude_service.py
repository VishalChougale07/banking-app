from anthropic import Anthropic
from typing import Dict, List
from config import settings

class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.CLAUDE_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def score_picks(self, picks: List[Dict], weather: Dict, time_of_day: str, location: str) -> List[Dict]:
        """Score picks 0-100 based on weather, time, and location (Zomato match score style)"""
        
        prompt = f"""
        You are a Zomato-style AI that scores restaurant and product picks.
        
        Current Weather: {weather}
        Time of Day: {time_of_day}
        Location: {location}
        
        Score each pick from 0-100 based on:
        - How well it matches current weather
        - Appropriateness for time of day
        - Local relevance
        
        Picks to score:
        {picks}
        
        Return ONLY a JSON array with fields: name, score (0-100), reason
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return self._parse_scores(response.content[0].text)
        except Exception as e:
            print(f"Claude scoring error: {e}")
            return picks  # Return unscore picks
    
    async def generate_insight(self, weather: Dict, time_of_day: str, location: str) -> str:
        """Generate weather-aware contextual insight (like Zomato's match insight)"""
        
        prompt = f"""
        Generate a short, catchy insight about what to eat or buy right now based on:
        Weather: {weather['current']['temperature']}°C, Raining: {weather['current']['is_raining']}
        Time: {time_of_day}
        Location: {location}
        
        Style: Keep it under 100 chars, casual, emoji-friendly. Like Zomato insights.
        Example: "Hot day vibes ☀️ → Ice cream & cold coffee trending today!"
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return "✨ Discover amazing picks nearby!"
    
    async def plan_outing(self, saved_picks: List[Dict], weather: Dict) -> str:
        """Claude plans a complete outing using saved picks"""
        
        prompt = f"""
        User has saved these picks:
        {saved_picks}
        
        Weather: {weather}
        
        Create a fun, optimized itinerary for their evening that:
        1. Suggests best order to visit
        2. Estimates time at each location
        3. Flags weather-related tips
        4. Recommends what to try
        
        Keep it conversational and practical.
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return "Great picks! Enjoy your outing!"
    
    def _parse_scores(self, response_text: str) -> List[Dict]:
        """Parse Claude's JSON response for scores"""
        import json
        try:
            # Extract JSON from response
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start != -1 and end > start:
                return json.loads(response_text[start:end])
        except:
            pass
        return []

claude_service = ClaudeService()