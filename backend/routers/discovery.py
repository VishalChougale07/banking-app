from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from services.database import DiscoveryPick, SavedPick, Order, get_db
from services.google_places_service import google_places_service
from services.weather_service import weather_service
from services.claude_service import claude_service
from typing import List, Dict
from datetime import datetime

router = APIRouter(prefix="/api/discovery", tags=["discovery"])

@router.get("/picks")
async def get_picks(
    shop_id: int = Query(...),
    location: str = Query("Mysuru"),
    latitude: float = Query(12.2958),
    longitude: float = Query(75.8235),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Get personalized picks with AI scores (Zomato-style).
    Combines restaurant + product picks scored by weather & time.
    """
    
    # Get weather
    weather = await weather_service.get_weather(latitude, longitude)
    
    # Search for restaurants
    restaurants = await google_places_service.search_restaurants(
        query="best rated",
        location=location,
        latitude=latitude,
        longitude=longitude
    )
    
    # Convert to pick format
    picks = []
    for rest in restaurants:
        picks.append({
            "name": rest.get("name"),
            "type": "restaurant",
            "description": rest.get("address"),
            "rating": rest.get("rating"),
            "reviews": rest.get("review_count"),
            "image": rest.get("photo_url"),
            "place_id": rest.get("place_id")
        })
    
    # Get time of day
    hour = datetime.now().hour
    time_of_day = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
    
    # Score with Claude
    scored_picks = await claude_service.score_picks(picks, weather, time_of_day, location)
    
    return {
        "picks": scored_picks[:10],
        "weather": weather,
        "location": location,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/ai-insight")
async def get_ai_insight(
    shop_id: int = Query(...),
    location: str = Query("Mysuru"),
    latitude: float = Query(12.2958),
    longitude: float = Query(75.8235)
) -> Dict:
    """
    Get weather-aware contextual AI insight (like Zomato's match insight).
    """
    
    weather = await weather_service.get_weather(latitude, longitude)
    
    hour = datetime.now().hour
    time_of_day = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
    
    insight = await claude_service.generate_insight(weather, time_of_day, location)
    
    return {
        "insight": insight,
        "weather": weather["current"],
        "time_of_day": time_of_day
    }

@router.post("/save-pick")
async def save_pick(
    shop_id: int = Query(...),
    pick_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Save a pick to user's curated list (like Zomato save for later).
    """
    
    try:
        saved_pick = SavedPick(shop_id=shop_id, pick_id=pick_id)
        db.add(saved_pick)
        await db.commit()
        
        return {"status": "saved", "pick_id": pick_id, "saved_at": datetime.now().isoformat()}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/saved-picks")
async def get_saved_picks(
    shop_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Retrieve all saved picks for a user.
    """
    
    try:
        stmt = select(SavedPick).where(SavedPick.shop_id == shop_id)
        result = await db.execute(stmt)
        saved_picks = result.scalars().all()
        
        return {
            "count": len(saved_picks),
            "saved_picks": [{
                "id": sp.id,
                "pick_id": sp.pick_id,
                "saved_at": sp.saved_at.isoformat()
            } for sp in saved_picks]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/plan-outing")
async def plan_outing(
    shop_id: int = Query(...),
    latitude: float = Query(12.2958),
    longitude: float = Query(75.8235),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Claude plans a complete outing using saved picks.
    Suggests order, timing, and weather tips (Zepto speed + Zomato intelligence).
    """
    
    try:
        # Get saved picks
        stmt = select(SavedPick).where(SavedPick.shop_id == shop_id)
        result = await db.execute(stmt)
        saved = result.scalars().all()
        
        # Get weather
        weather = await weather_service.get_weather(latitude, longitude)
        
        # Plan with Claude
        plan = await claude_service.plan_outing(
            [{"id": s.pick_id} for s in saved],
            weather
        )
        
        return {
            "plan": plan,
            "picks_count": len(saved),
            "estimated_time_hours": len(saved) * 1.5,
            "weather_alert": "☔ Rain expected" if weather["current"]["is_raining"] else "☀️ Clear skies"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))