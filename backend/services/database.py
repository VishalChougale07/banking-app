from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, JSON, Boolean
from datetime import datetime
from config import settings

Base = declarative_base()

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Shop(Base):
    __tablename__ = "shops"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop_name: Mapped[str] = mapped_column(String(255))
    shop_url: Mapped[str] = mapped_column(String(255), unique=True)
    access_token: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DiscoveryPick(Base):
    __tablename__ = "discovery_picks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int]
    pick_type: Mapped[str] = mapped_column(String(50))  # "restaurant" or "product"
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    location: Mapped[str] = mapped_column(String(255))
    rating: Mapped[float] = mapped_column(Float)
    review_count: Mapped[int] = mapped_column(Integer)
    ai_match_score: Mapped[int] = mapped_column(Integer, default=0)  # 0-100 like Zomato
    weather_adjusted_score: Mapped[int] = mapped_column(Integer, default=0)
    delivery_time_minutes: Mapped[int] = mapped_column(Integer, default=10)  # Zepto-style
    image_url: Mapped[str] = mapped_column(String(500))
    google_place_id: Mapped[str] = mapped_column(String(255), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SavedPick(Base):
    __tablename__ = "saved_picks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int]
    pick_id: Mapped[int]
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int]
    pick_id: Mapped[int]
    order_status: Mapped[str] = mapped_column(String(50))  # pending, confirmed, preparing, on_way, delivered
    estimated_delivery_minutes: Mapped[int] = mapped_column(Integer)
    actual_delivery_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session