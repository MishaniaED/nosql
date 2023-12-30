instance = new Mongo("host.docker.internal:27017");
db = instance.getDB("mongo_db_node_01");

config = {
    "_id": "docker-replicaset",
    "members": [
        {
            "_id": 0,
            "host": "host.docker.internal:27017"
        },
        {
            "_id": 1,
            "host": "host.docker.internal:27018"
        },
        {
            "_id": 2,
            "host": "host.docker.internal:27019"
        }
    ]
};

try {
    rs.conf()
}
catch {
    rs.initiate(config);
}