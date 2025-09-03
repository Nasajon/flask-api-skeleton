import os
import redis

from typing import Any

redis_client = redis.Redis(host="192.168.3.42", port=6379, db=0)

APP_NAME = os.environ["APP_NAME"]


def k(*parts: str) -> str:
    return APP_NAME + ":" + ":".join(parts)


def get_redis(*args: str) -> Any:
    value = redis_client.get(k(*args))
    return value.decode("utf-8")


def set_redis(*args) -> None:
    value = args[-1]
    redis_client.set(k(*args[:-1]), value)


set_redis("ping", "pong")
print(get_redis(("ping")))
