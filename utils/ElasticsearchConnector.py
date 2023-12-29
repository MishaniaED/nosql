import os
from asyncio import exceptions
from utils.MongoDBSetup import async_db

from elasticsearch import AsyncElasticsearch, logger, NotFoundError

elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


async def connect_and_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
    except Exception as ex:
        print(f'Cant connect to elasticsearch: {ex}')


async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()


def create_train_index():
    """Creating an index for trains"""
    try:
        body = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "route_id": {"type": "integer"},
                    "type": {"type": "keyword"},
                    "departure_date": {"type": "date"},
                    "arrival_date": {"type": "date"},
                }
            }
        }
        response = elasticsearch_client.indices.create(index="trains", body=body, ignore=400)
        logger.info("Train index created successfully.")
        return response
    except Exception as e:
        logger.error(f"Error creating train index: {e}")
        return None


async def add_train_to_index(train_data):
    """Adding train information to the index"""
    try:
        route_id = train_data["route_id"]
        route = await async_db.routes.find_one({"route_id": route_id})
        stations = route["stations"]
        train_data["stations"] = stations

        response = elasticsearch_client.index(index="trains", body=train_data)
        logger.info("Train data added to index successfully.")
        return response
    except Exception as e:
        logger.error(f"Error adding train data to index: {e}")
        return None


def search_trains(departure_station_id, arrival_station_id, departure_date):
    """Search for trains according to the specified criteria"""
    try:
        query = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"term": {"stations": departure_station_id}},
                                {"term": {"stations": arrival_station_id}},
                            ],
                            "minimum_should_match": 2,
                        }
                    },
                    {"range": {"departure_date": {"gte": departure_date}}},
                ]
            }
        }
        response = elasticsearch_client.search(index="trains", body={"query": query})
        logger.info("Search for trains executed successfully.")
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception as e:
        logger.error(f"Error searching trains: {e}")
        return []


def delete_train_from_index(train_id):
    """Deleting train information from the index by ID"""
    try:
        query = {
            "query": {
                "term": {"id": train_id}
            }
        }
        response = elasticsearch_client.delete_by_query(index="trains", body=query)
        logger.info("Train data deleted from index successfully.")
        return response
    except NotFoundError:
        logger.error(f"Train data not found in index for id: {train_id}")
        return None
    except Exception as e:
        logger.error(f"Error deleting train data from index: {e}")
        return None
