import aiohttp
import hashlib
import hmac
from config import settings
from typing import Dict, Optional

class ShopifyService:
    async def verify_webhook(self, raw_body: bytes, x_shopify_hmac_header: str) -> bool:
        """Verify Shopify webhook authenticity"""
        digest = hmac.new(
            settings.SHOPIFY_API_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).digest()
        
        import base64
        computed_hmac = base64.b64encode(digest).decode()
        return computed_hmac == x_shopify_hmac_header
    
    async def get_access_token(self, code: str, shop: str) -> Optional[str]:
        """Exchange authorization code for access token (OAuth)"""
        url = f"https://{shop}/admin/oauth/access_token"
        
        payload = {
            "client_id": settings.SHOPIFY_API_KEY,
            "client_secret": settings.SHOPIFY_API_SECRET,
            "code": code
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("access_token")
        except Exception as e:
            print(f"Shopify OAuth error: {e}")
        
        return None
    
    async def get_products(self, shop: str, access_token: str, limit: int = 10) -> list:
        """Fetch merchant's products from Shopify store"""
        url = f"https://{shop}/admin/api/2024-01/products.json"
        
        headers = {
            "X-Shopify-Access-Token": access_token
        }
        
        params = {
            "limit": limit,
            "status": "active"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("products", [])
        except Exception as e:
            print(f"Shopify products fetch error: {e}")
        
        return []
    
    async def add_product_image(self, shop: str, access_token: str, product_id: str, image_url: str) -> bool:
        """Add generated AI image to Shopify product"""
        url = f"https://{shop}/admin/api/2024-01/products/{product_id}/images.json"
        
        headers = {
            "X-Shopify-Access-Token": access_token
        }
        
        payload = {
            "image": {
                "src": image_url,
                "alt": "AI Generated Lifestyle Photo"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status in [200, 201]
        except Exception as e:
            print(f"Shopify image upload error: {e}")
        
        return False

shopify_service = ShopifyService()