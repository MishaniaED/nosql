import asyncio

# from utils.HazelcastConnector import connect_and_init_memcached, close_memcached_connect
# from utils.MongoDBSetup import connect_and_init_mongo, close_mongo_connect, setup_sharding
from utils.ElasticsearchConnector import connect_and_init_elasticsearch, close_elasticsearch_connect


async def startup():
    init_elasticsearch_future = connect_and_init_elasticsearch()
    await asyncio.gather(init_elasticsearch_future)


async def shutdown():
    await close_elasticsearch_connect()
