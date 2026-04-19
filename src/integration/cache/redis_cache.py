import json
import aioredis
from src.config.config import settings
from src.logger.logger import logger

# -------------------------
# Redis connection
# -------------------------
redis = aioredis.from_url(settings.redis_url, decode_responses=True)

# -------------------------
# Cache promotion
# -------------------------
async def cache_promotion(promo_id: str, data: dict, ttl: int = 3600):
    try:
        await redis.set(f"promotion:{promo_id}", json.dumps(data), ex=ttl)
        logger.info(f"Cached promotion {promo_id} for {ttl} seconds")
    except Exception as e:
        logger.error(f"Failed to cache promotion {promo_id}: {e}")

# -------------------------
# Get cached promotion
# -------------------------
async def get_cached_promotion(promo_id: str):
    try:
        cached = await redis.get(f"promotion:{promo_id}")
        if cached:
            return json.loads(cached)
        return None
    except Exception as e:
        logger.error(f"Failed to get cached promotion {promo_id}: {e}")
        return None

# -------------------------
# Invalidate cache
# -------------------------
async def invalidate_promotion_cache(promo_id: str):
    try:
        await redis.delete(f"promotion:{promo_id}")
        logger.info(f"Invalidated cache for promotion {promo_id}")
    except Exception as e:
        logger.error(f"Failed to invalidate cache for promotion {promo_id}: {e}")
