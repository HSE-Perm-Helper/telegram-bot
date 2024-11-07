from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

import env

storage = MemoryStorage()

if env.is_prod:
    redis = Redis(host=env.RD_HOST, port=env.RD_PORT, db=env.RD_DB)
    storage = RedisStorage(redis=redis)

bot = Bot(env.bot_token)
dp = Dispatcher(storage=storage)
