import logging
import coloredlogs
import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hazelcast")
coloredlogs.install()


def get_hazelcast_client():
    try:
        client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=["hazelcast:5701"])
        logger.info("Connected to the Hazelcast cluster")
        return client
    except Exception as e:
        logger.error(f"Error connecting to Hazelcast cluster: {e}")
        raise


hazelcast_client = get_hazelcast_client()


def cache_station(station_id, station_data):
    try:
        stations_map = hazelcast_client.get_map("stations")
        future_station_data = stations_map.put(station_id, station_data)
        result = future_station_data.result()
        logger.info(f"Station data cached for station ID: {station_id}")
        return result
    except Exception as e:
        logger.error(f"Error caching station data for station ID {station_id}: {e}")
        raise


async def get_cached_station(station_id):
    try:
        stations_map = hazelcast_client.get_map("stations")
        future_station_data = stations_map.get(station_id)
        station_data = future_station_data.result()

        if station_data is None:
            logger.warning(f"No data found in cache for station ID: {station_id}")
            return None

        logger.info(f"Retrieved data from cache for station ID: {station_id}")
        return station_data
    except Exception as e:
        logger.error(f"Error retrieving station data for station ID {station_id}: {e}")
        raise


def lock_ticket(ticket_id):
    try:
        lock_key = f"myLock@group{ticket_id}"
        ticket_lock = hazelcast_client.cp_subsystem.get_lock(lock_key).blocking()
        fence = ticket_lock.try_lock()

        if fence != ticket_lock.INVALID_FENCE:
            logger.info(f"Ticket ID {ticket_id} locked successfully.")
            return True
        logger.warning(f"Ticket ID {ticket_id} is already locked.")
        return False
    except Exception as e:
        logger.error(f"Error locking ticket ID {ticket_id}: {e}")
        raise


def unlock_ticket(ticket_id):
    try:
        lock_key = f"myLock@group{ticket_id}"
        ticket_lock = hazelcast_client.cp_subsystem.get_lock(lock_key).blocking()
        ticket_lock.unlock()
        logger.info(f"Ticket ID {ticket_id} unlocked successfully.")
    except Exception as e:
        logger.error(f"Error unlocking ticket ID {ticket_id}: {e}")
        raise
