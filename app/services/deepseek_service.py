import httpx
from typing import List, Dict
from ..config import settings
from ..models import Product

class DeepSeekService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL

    async def generate_product_context(self, products: List[Product]) -> str:
        """Generate context string from merchant's products"""
        if not products:
            return "No products available."

        context = "Available products:\n"
        for product in products:
            context += f"- {product.name}: {product.description or 'No description'} (Price: ${product.price})\n"
        return context

    async def chat(self, messages: List[Dict[str, str]], product_context: str) -> str:
        """Send chat request to DeepSeek API"""
        if not self.api_key:
            return "DeepSeek API key not configured. Please contact the administrator."

        # Prepare system message with product context
        system_message = {
            "role": "system",
            "content": f"You are a helpful furniture shopping assistant. Help customers find the right furniture based on their needs. Here are the products available from this merchant:\n\n{product_context}\n\nProvide recommendations based on these products and the customer's requirements."
        }

        # Combine system message with user messages
        full_messages = [system_message] + messages

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": full_messages,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            return f"Error communicating with DeepSeek API: {e.response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

deepseek_service = DeepSeekService()
