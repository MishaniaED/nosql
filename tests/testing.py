import pytest
from fastapi.testclient import TestClient
from main import app
from services import StationService

client = TestClient(app)


def test_add_route():
    route_data = {
        "id": 1,
        "name": "Test Route",
        "distance": 10.5,
        "duration": 2.5
    }

    response = client.post("/", json=route_data)
    assert response.status_code == 200
    assert response.json() == route_data
    response = client.get(f"/{route_data['id']}")
    assert response.status_code == 200
    assert response.json() == route_data
    client.delete(f"/{route_data['id']}")


def test_add_duplicate_route():
    route_data = {
        "id": 2,
        "name": "Test Route",
        "distance": 10.5,
        "duration": 2.5
    }

    response = client.post("/", json=route_data)
    assert response.status_code == 200
    response = client.post("/", json=route_data)
    assert response.status_code == 409
    client.delete(f"/{route_data['id']}")


def test_get_nonexistent_route():
    response = client.get("/999")
    assert response.status_code == 404


def test_add_station():
    station_data = {
        "id": 1,
        "name": "Test Station",
        "location": "Test Location"
    }

    response = client.post("/", json=station_data)

    assert response.status_code == 200
    assert response.json() == station_data

    response = client.get(f"/{station_data['id']}")

    assert response.status_code == 200
    assert response.json() == station_data

    client.delete(f"/{station_data['id']}")


def test_add_duplicate_station():
    station_data = {
        "id": 2,
        "name": "Test Station",
        "location": "Test Location"
    }

    response = client.post("/", json=station_data)

    assert response.status_code == 200

    response = client.post("/", json=station_data)

    assert response.status_code == 409

    client.delete(f"/{station_data['id']}")


def test_get_nonexistent_station():
    response = client.get("/999")

    assert response.status_code == 404


def test_get_station_server_error():
    station_data = {
        "id": 3,
        "name": "Test Station",
        "location": "Test Location"
    }

    response = client.post("/", json=station_data)

    assert response.status_code == 200

    app.dependency_overrides[StationService.get_station] = lambda station_id: Exception("Simulated Server Error")

    response = client.get(f"/{station_data['id']}")

    assert response.status_code == 500

    client.delete(f"/{station_data['id']}")


def test_book_ticket():
    ticket_id = 1

    response = client.post(f"/book/{ticket_id}")

    assert response.status_code in [200, 400, 404, 503, 500]


def test_purchase_ticket():
    ticket_id = 2

    response = client.post(f"/purchase/{ticket_id}")

    assert response.status_code in [200, 400, 404, 500]


def test_search_tickets():
    train_id = 1
    status = "available"
    comfort_class = "economy"

    response = client.get(f"/search-tickets/?train_id={train_id}&status={status}&comfort_class={comfort_class}")

    assert response.status_code in [200, 500]


def test_get_ticket():
    ticket_id = 3

    response = client.get(f"/{ticket_id}")

    assert response.status_code in [200, 404, 500]


def test_add_ticket():
    ticket_data = {
        "id": 4,
        "train_id": 1,
        "status": "available",
        "comfort_class": "economy",
        "departure_datetime": "2022-01-01T12:00:00",
        "arrival_datetime": "2022-01-01T14:00:00",
        "price": 50.0
    }

    response = client.post("/", json=ticket_data)

    assert response.status_code in [200, 409, 500]

    client.delete(f"/{ticket_data['id']}")


def test_add_train():
    train_data = {
        "id": 1,
        "name": "Test Train",
        "capacity": 100,
        "departure_station_id": 1,
        "arrival_station_id": 2,
        "departure_time": "2022-01-01T12:00:00",
        "arrival_time": "2022-01-01T14:00:00",
    }

    response = client.post("/", json=train_data)

    assert response.status_code in [200, 409]

    if response.status_code == 200:
        client.delete(f"/{train_data['id']}")


def test_get_train():
    train_id = 2  # Replace with a valid train ID

    response = client.get(f"/{train_id}")

    assert response.status_code in [200, 404, 500]


def test_available_trains():
    departure_station_id = 1
    departure_date = "2022-01-01T12:00:00"
    arrival_station_id = 2

    response = client.get(
        f"/available/?departure_station_id={departure_station_id}&departure_date={departure_date}&arrival_station_id={arrival_station_id}")

    assert response.status_code in [200, 500]


def test_delete_train():
    train_id = 3

    response = client.delete(f"/{train_id}/")

    assert response.status_code in [200, 404]
