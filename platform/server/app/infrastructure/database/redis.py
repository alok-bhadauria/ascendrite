import logging

logger = logging.getLogger(__name__)

class RedisManagerPlaceholder:
    def __init__(self):
        self.is_connected = False
    
    def ping(self) -> bool:
        logger.info("Redis placeholder ping check")
        return True

redis_manager = RedisManagerPlaceholder()

def get_redis():
    return redis_manager
