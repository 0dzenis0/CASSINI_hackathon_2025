from pydantic import BaseModel

class Vitals(BaseModel):
    user_id: str
    timestamp: float
    heart_rate: int
    lat: float
    lon: float
