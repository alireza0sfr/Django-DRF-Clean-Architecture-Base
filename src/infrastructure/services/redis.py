from django_redis import get_redis_connection
from django.core.cache import cache
from decouple import config


from application.interfaces.services.redis import IRedisService


class RedisService(IRedisService):
    @staticmethod
    def delete_by_prefix(key: str):
        if config("USE_DUMMY_CACHE", cast=bool):
            return

        redis_conn = get_redis_connection("default")
        all_keys = redis_conn.keys("*")

        for k in all_keys:
            cache_key = k.decode("utf-8").split(":1:")[1]
            if key in cache_key:
                cache.delete(cache_key)
