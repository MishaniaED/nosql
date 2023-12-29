import datetime
import random
import requests

url_base = "http://localhost:8000/"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


def generate_stations(number):
    url = url_base + "station/"
    country_names = ["Russia"]
    area_names = [
        "Moscow",
        "St. Petersburg",
        "Kazan",
        "Yekaterinburg",
        "Novosibirsk",
        "Vladivostok",
        "Sochi",
        "Nizhny Novgorod",
        "Samara",
        "Irkutsk",
        "Kaliningrad",
        "Rostov-on-Don",
        "Volgograd",
        "Murmansk",
        "Ufa",
        "Krasnoyarsk",
        "Omsk",
        "Perm",
        "Tomsk",
        "Saransk"
    ]
    names = [
        "Moskovskiy Vokzal",
        "Saint Petersburg-Glavnyy",
        "Yaroslavskiy Vokzal",
        "Kazanskiy Vokzal",
        "Leningradskiy Vokzal",
        "Kurskiy Vokzal",
        "Belorusskiy Vokzal",
        "Savyolovskiy Vokzal",
        "Paveletskiy Vokzal",
        "Kievskiy Vokzal",
        "Rizhskiy Vokzal",
        "Baltiyskiy Vokzal",
        "Finlyandskiy Vokzal",
        "Novosibirsk-Glavnyy",
        "Irkutsk-Passazhirskiy",
        "Krasnoyarsk-Glavnyy",
        "Vladivostok-Passazhirskiy",
        "Nizhniy Novgorod-Glavnyy",
        "Samara-Glavnyaya",
        "Sochi-Vokzal"
    ]

    for id in range(0, number):
        response = requests.post(url, json={
            "id": id,
            "country_name": country_names[0],
            "area_name": area_names[random.randint(0, len(area_names))],
            "name": names[random.randint(0, len(names))],
        }, headers=headers)
        if response.status_code == 200:
            print(f"Object {id} created")
        else:
            print(f"Error while creating {id}: {response.text}")


def generate_routes(number):
    url = url_base + "route/"
    names = ["Golden Ring",
             "Siberian Express",
             "Great Ural",
             "Volga-Volga",
             "White Nights",
             "Trans-Siberian Odyssey",
             "Amur Wind",
             "St. Petersburg Fairy Tale",
             "Winter Spectacle",
             "Caucasian Trail",
             "Baikal Breeze",
             "Altai Express",
             "Taiga Trails",
             "Sunny South",
             "Elbrus Express",
             "Omsk Star",
             "Ladoga Breeze",
             "Crimean Journey",
             "Ural Pass",
             "Far East Expedition"]

    types = ["Tourist", "Express", "Freight"]

    for id in range(0, number):
        response = requests.post(url, json={
            "id": id,
            "stations_id": random.sample(range(200), random.randint(5, 20)),
            "name": names[random.randint(0, len(names))],
            "type": types[random.randint(0, len(types))],
            "travel_time": str(datetime.datetime.now()),
            "travel_distance": random.randint(80, 1000),
        }, headers=headers)

        if response.status_code == 200:
            print(f"Object {id} created")
        else:
            print(f"Error while creating {id}: {response.text}")


def generate_trains(number):
    url = url_base + "train/"

    types = ["Lastochka", "Cargo"]

    for id in range(0, number):
        response = requests.post(url, json={
            "id": id,
            "route_id": 0,
            "type": types[random.randint(0, len(types))],
            "departure_data": str(datetime.datetime.now()),
            "arrival_data": str(datetime.datetime.now())
        }, headers=headers)
        if response.status_code == 200:
            print(f"Object {id} created")
        else:
            print(f"Error while creating {id}: {response.text}")


def generate_tickets(number):
    url = url_base + "ticket/"
    comfort_class = ["economy", "business"]
    passenger_data = [
        "Ivan Petrov",
        "Maria Ivanova",
        "Sergei Smirnov",
        "Ekaterina Kuznetsova",
        "Dmitriy Popov",
        "Olga Sokolova",
        "Andrei Ivanov",
        "Natalia Fedorova",
        "Mikhail Sidorov",
        "Anna Volkova",
        "Alexei Petrov",
        "Yulia Sokolova",
        "Pavel Smirnov",
        "Tatiana Ivanova",
        "Nikolai Fedorov",
        "Elena Kuznetsova",
        "Vladimir Popov",
        "Svetlana Sokolova",
        "Igor Ivanov"
    ]
    for id in range(0, number):
        response = requests.post(url, json={
            "id": id,
            "train_id": random.randint(0, 1000),
            "status": "free",
            "price": random.randint(800, 7000),
            "passenger_data": passenger_data[random.randint(0, len(passenger_data))],
            "comfort_class": comfort_class[random.randint(0, len(comfort_class))],
            "carriage_number": random.randint(1, 21),
            "seat_number": random.randint(1, 41),
            "booking_date": str(datetime.datetime.now()),
            "payment_date": str(datetime.datetime.now())
        }, headers=headers)
        if response.status_code == 200:
            print(f"Object {id} created")
        else:
            print(f"Error while creating {id}: {response.text}")


if __name__ == "__main__":
    generate_stations(200)
    generate_routes(500)
    generate_trains(1000)
    generate_tickets(5000)
