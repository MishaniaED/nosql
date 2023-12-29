import asyncio

from utils.HazelcastConnector import connect_and_init_memcached, close_memcached_connect
# from utils.MongoDBSetup import connect_and_init_mongo, close_mongo_connect
from utils.ElasticsearchConnector import connect_and_init_elasticsearch, close_elasticsearch_connect


async def startup():
    init_mongo_future = connect_and_init_mongo()
    init_elasticsearch_future = connect_and_init_elasticsearch()
    # await asyncio.gather(init_mongo_future, init_elasticsearch_future)
    await asyncio.gather(init_elasticsearch_future)
    # connect_and_init_memcached()


async def shutdown():
    # close_mongo_connect()
    # close_memcached_connect()
    await close_elasticsearch_connect()
