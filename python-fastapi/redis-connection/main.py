import os
import redis
import time
from fastapi import Depends, FastAPI

from config.db import pool

app = FastAPI()

USING_DEPS_INJECTION = True
USING_POOL = True

# Approach #1: Create global variable for redis
global_cache = redis.Redis(
  host=os.environ.get('REDIS_HOST', 'localhost'), 
  port=os.environ.get('REDIS_PORT', 6379), 
  db=os.environ.get('REDIS_DB', 0), 
  decode_responses=True
)

def get_redis():
  print("Using Pool" if USING_POOL else "Using Direct Connect")
  if USING_POOL:
    # Approach #2: Create redis connection pool
    return redis.Redis(connection_pool=pool)
  else:
    # Approach #3: Create redis connection directly
    return redis.Redis(
      host=os.environ.get('REDIS_HOST', 'localhost'), 
      port=os.environ.get('REDIS_PORT', 6379), 
      db=os.environ.get('REDIS_DB', 0), 
      decode_responses=True
    )

@app.get("/items/{item_id}")
async def read_item(
    item_id: int, 
    deps_inj_cache = Depends(get_redis)
  ):
  status = deps_inj_cache.get(item_id) if USING_DEPS_INJECTION else global_cache.get(item_id)
  return {"item_name": status}

@app.get("/items-non-async/{item_id}")
def read_item(
    item_id: int, 
    deps_inj_cache = Depends(get_redis)
  ):
  status = deps_inj_cache.get(item_id) if USING_DEPS_INJECTION else global_cache.get(item_id)
  return {"item_name": status}



@app.put("/items/{item_id}")
# Remove async keyword, and it will not block you
async def update_item(
    item_id: int,
    deps_inj_cache = Depends(get_redis)
  ):
  deps_inj_cache.set(item_id, "available") if USING_DEPS_INJECTION else global_cache.set(item_id, "available")
  time.sleep(10) # Intentional to check if this will block other endpoint
  return {"status": "available", "item_id": item_id}
