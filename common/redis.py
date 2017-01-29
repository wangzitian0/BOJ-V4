
import redis


pool = redis.ConnnectionPool(host='127.0.0.1', port=6379)
r = redis.StrictRedis(connection_pool=pool)


