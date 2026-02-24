from upstash_redis  import Redis
from app.config import settings
import json
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        if settings.redis_upstash_rest_url and settings.redis_upstash_rest_token:
            self.redis = Redis(
                 url=settings.redis_upstash_rest_url,
                 token=settings.redis_upstash_rest_token
            )
            self.enabled =True
            logger.info("Redis cache enabled")
        else:
            self.redis = None
            self.enabled = False
            logger.warning("Redis not configured - caching disabled")    
    def get(self, key:str) ->Optional[Any]:
        if not self.enabled:
            return None
        try:
            value = self.redis.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
        

    def set(self , key:str, value:Any, ttl=300):
        if not self.enabled:
            return

        try:
            self.redis.set(key, json.dumps(value), ex=ttl)  
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")


    def delete(self , key:str):
        if not self.enabled:
            return
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")        


cache_service = CacheService()
