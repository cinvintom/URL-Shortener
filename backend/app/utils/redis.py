from app.core.config import settings
import redis
import json

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def get_cached_url(short_url: str):
    cached = redis_client.get(f"url:{short_url}")
    if cached:
        return json.loads(cached)
    return None


def cache_url(short_url: str, original_url: str, ttl: int = 3600):
    redis_client.setex(
        f"url:{short_url}", 
        ttl, 
        json.dumps({"original_url": original_url})
    )