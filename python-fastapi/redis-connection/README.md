# How to use redis connection pool with FastAPI

## How to run

I'm using `pipenv`, so if you like me, just `pipenv install` as usual. If not, `pip install -r requirements.txt` to satisfy the deps.

We can run redis from docker so we don't have to install it. Run `docker-compose up` and let it run for you. I run redis with **logging level: debug**. So we can see if a new connection is established.

After that, we can run our FastAPI app, `uvicorn main:app --reload`. I suggest you run in a split view (side by side) with docker compose command.

## How to experiment

Open `main.py`, find `USING_DEPS_INJECTION` and `USING_POOL` and try to toggle the value.

* `USING_DEPS_INJECTION = False` will use global declaration of redis and ignore the dependency injection variable.
  * Hit the `PUT` endpoint then hit the `GET` endpoint. The latter will be blocked by the former.
  * Remove `async` in `PUT` function, it will not block anymore.
* `USING_DEPS_INJECTION = True` and `USING_POOL = False` will use dependency injection and return a new redis client connection.
  * Even with `async` in `PUT` function, it will not block. But in the Redis log, we will have `2 clients connected`.
  * The connection will be close after the function exit
* `USING_DEPS_INJECTION = True` and `USING_POOL = False` will use dependency injection and return a redis client with connection pooling.
  * Even with `async` in `PUT` function, it will not block. In the Redis log, we will have `1 clients connected`.
  * In the redis log, even without new request, there will be 1 (or more) clients connected until you stop the FastAPI app.