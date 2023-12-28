import logging
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hazelcast")


def get_hazelcast_client():
    client = hazelcast.HazelcastClient()
    logger.info("Connected to cluster")
    return client


hazelcast_client = get_hazelcast_client()


def cache_station(station_id, station_data):
    pass


async def get_cached_station(station_id):
    pass


def lock_ticket(ticket_id):
    pass


def unlock_ticket(ticket_id):
    pass
