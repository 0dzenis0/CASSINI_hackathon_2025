from fastapi import APIRouter, Depends
from .models import Vitals
from .services import cassini
import asyncpg, os, json, redis.asyncio as redis

router = APIRouter()

DB_URL = os.getenv("DATABASE_URL")
REDIS = redis.from_url(os.getenv("REDIS_URL"))

@router.post("/api/vitals")
async def post_vitals(v: Vitals):
    # save to db
    conn = await asyncpg.connect(DB_URL)
    await conn.execute(
        "INSERT INTO vitals(user_id,time,hr,lat,lon) VALUES($1,to_timestamp($2),$3,$4,$5)",
        v.user_id, v.timestamp, v.heart_rate, v.lat, v.lon
    )
    await conn.close()
    # fetch env
    env = await cassini.get_env(v.lat, v.lon)
    risk = calc_risk(v.heart_rate, env["aqi"], env["temperature"])
    if risk > 0.8:
        await REDIS.publish("alerts", json.dumps({"user": v.user_id, "risk": risk}))
    return {"risk": risk}

def calc_risk(hr, aqi, temp):
    risk = (hr/180) * 0.5 + (aqi/300) * 0.3 + max(0, (temp-30)/20) * 0.2
    return min(risk, 1.0)
