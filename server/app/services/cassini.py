"""Fetches environmental data from Copernicus/Cassini APIs"""
import httpx, os

CASSINI_ENDPOINT = "https://api.cassini.eu/data"
API_KEY = os.getenv("CASSINI_API_KEY")

async def get_env(lat: float, lon: float):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            CASSINI_ENDPOINT,
            params={"lat": lat, "lon": lon, "apikey": API_KEY}, timeout=15
        )
        r.raise_for_status()
        data = r.json()
        # Simplified: return AQI & temperature
        return {
            "aqi": data.get("aqi", 50),
            "temperature": data.get("temp", 20),
        }
