# 🚀 Shopify Discovery App
## AI-Powered Restaurant & Product Discovery (Zomato + Zepto)

**Combines the best of both worlds:**
- 🎯 **Zomato features**: AI match scores (0-100), social proof, discovery UX
- ⚡ **Zepto features**: Speed-first interface, 10-min delivery promise, real-time tracking

---

## 🔌 Multi-API Architecture

| API | Purpose | Status |
|-----|---------|--------|
| **Claude AI** | Personalized scoring, insights, outing planning | ✅ Active |
| **Google Places** | Live restaurant data (ratings, reviews, hours) | ✅ Active |
| **Open-Meteo** | Real-time weather (free, no API key) | ✅ Active |
| **PostgreSQL** | Persistent data storage | ✅ Ready |
| **Shopify Admin API** | Product sync, orders, inventory | ✅ Ready |

---

## 📦 Backend Features

✅ **Discovery Feed**
- Get personalized picks with weather-adjusted AI scores
- Real-time restaurant data from Google Places
- Context-aware rankings (weather + time + location)

✅ **AI Insights**
- Weather-aware contextual insights
- 100-char catchy recommendations
- Emoji-friendly messaging

✅ **Save & Plan**
- Save picks to curated list
- Claude plans complete outings
- Suggests order, timing, weather tips

✅ **Data Models**
- Shop (merchant stores)
- DiscoveryPick (restaurants + products)
- SavedPick (user curations)
- Order (Zepto-style delivery tracking)

---

## 🚀 Quick Start

### Setup

```bash
# 1. Clone repo
git clone https://github.com/VishalChougale07/shopify-discovery-app.git
cd shopify-discovery-app

# 2. Create .env from .env.example
cp .env.example .env

# 3. Fill in your API keys:
# - Shopify API Key & Secret (from partners.shopify.com)
# - Google Places API Key (from cloud.google.com)
# - Claude API Key (from console.anthropic.com)
# - PostgreSQL connection string

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start server
python main.py
```

### API Endpoints

**Get Personalized Picks** (with AI scores)
```
GET /api/discovery/picks?shop_id=1&location=Mysuru&latitude=12.2958&longitude=75.8235
```

**Get AI Insight** (weather-aware recommendation)
```
GET /api/discovery/ai-insight?shop_id=1&location=Mysuru
```

**Save a Pick**
```
POST /api/discovery/save-pick?shop_id=1&pick_id=123
```

**Get Saved Picks**
```
GET /api/discovery/saved-picks?shop_id=1
```

**Plan Your Outing** (Claude plans your day)
```
POST /api/discovery/plan-outing?shop_id=1&latitude=12.2958&longitude=75.8235
```

---

## 📊 Response Examples

### Get Picks Response
```json
{
  "picks": [
    {
      "name": "Pankhii",
      "type": "restaurant",
      "rating": 4.8,
      "reviews": 692,
      "score": 92,
      "reason": "Perfect for hot weather - AC inside, great for brunch"
    }
  ],
  "weather": {
    "current": {"temperature": 35, "is_raining": false}
  }
}
```

### AI Insight Response
```json
{
  "insight": "☀️ Hot day vibes → Ice cream & cold coffee trending!",
  "weather": {"temperature": 35, "is_raining": false},
  "time_of_day": "afternoon"
}
```

---

## 🎯 Next Steps

- [ ] Build frontend dashboard (Next.js + Tailwind)
- [ ] Implement Shopify OAuth flow
- [ ] Add real-time order tracking
- [ ] Integrate Zepto delivery partner API
- [ ] Deploy to production (Docker + Railway)

---

## 📄 License

MIT
