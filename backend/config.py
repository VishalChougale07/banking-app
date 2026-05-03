from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys & Credentials
    SHOPIFY_API_KEY: str
    SHOPIFY_API_SECRET: str
    SHOPIFY_SCOPES: str = "write_products,read_products,write_orders,read_orders"
    
    GOOGLE_PLACES_API_KEY: str
    CLAUDE_API_KEY: str
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/shopify_discovery"
    
    # App URLs
    SHOPIFY_CALLBACK_URL: str = "http://localhost:8000/api/auth/callback"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Server
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()