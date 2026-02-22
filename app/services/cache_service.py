from upstash_redis  import Redis
from app.config import settings
import json
from typing import Optional, Any


class CacheService:
    def __init__(self):
        if settings.redis_upstash_rest_url and settings.redis_upstash_rest_token:
            self.redis = Redis(
                rest_url=settings.redis_upstash_rest_url,
                rest_token=settings.redis_upstash_rest_token
            )
            self.enabled =True
        else:
            self.redis = None
            self.enabled = False
            print("Redis not configured properly")    
    def get(self, key:str) ->Optional[Any]:
        if not self.enabled:
            return None
        try:
            value = self.redis.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception as e:
            print(f" cache get error: {e}")
            return None
        

    def set(self , key:str, value:Any, ttl=300):
        if not self.enabled:
            return

        try:
            self.redis.set(key, json.dumps(value), ex=ttl)  
        except Exception as e:
            print(f"cache set error: {e}")


    def delete(self , key:str):
        if not self.enabled:
            return
        try:
            self.redis.delete(key)
        except Exception as e:
            print(f"cache delete error: {e}")        


cache_service = CacheService()
