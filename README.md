# HeartSight
Real‑time Cassini‑enabled early‑warning system for elderly travelers with tachycardia.

### Quick Start
```bash
# backend
cp .env.example .env
docker compose up -d --build
# mobile
cd mobile
./gradlew assembleDebug
---
## .env.example
```env
DATABASE_URL=postgresql://heartsight:heartsight@db:5432/heartsight_db
CASSINI_API_KEY=your_cassini_key
REDIS_URL=redis://cache:6379/0
