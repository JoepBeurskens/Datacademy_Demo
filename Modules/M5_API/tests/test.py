from Modules.M5_API.src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome at the Module 5 API!"


def test_get_customer():
    response = client.get("/get-customer/0")
    assert response.status_code == 200
    assert response.json() == {
        "firstName": "John",
        "lastName": "Doe",
        "address": "1948 Conifer Drive"}


def test_get_customer_by_name():
    response = client.get("/get-customer-by-name/Booker")
    assert response.status_code == 200
    assert response.json() == {
        "firstName": "Deshawn",
        "lastName": "Booker",
        "address": "183 Jadewood Farms"}


def test_get_customers():
    response = client.get("/get-customers/")
    assert response.status_code == 200
    assert response.json() == {
        "0": {
            "firstName": "John",
            "lastName": "Doe",
            "address": "1948 Conifer Drive"
            },
        "1": {
            "firstName": "Arthur",
            "lastName": "Holmes",
            "address": "2149 Stockert Hollow Road"
            },
        "2": {
            "firstName": "Jamie",
            "lastName": "Dean",
            "address": "4883 White Lane"
            }
        }


def test_create_customer():
    data = {
        "firstName": "Jan",
        "lastName": "Janssen",
        "address": "Kerkstraat 10"
        }

    response = client.post("/create-customer/21", json=data)

    assert response.status_code == 200
    assert response.json() == data
    assert client.get("/get-customer/21").json() == data


def test_create_customer_auto_increment():
    data = {
        "firstName": "Fred",
        "lastName": "De Vries",
        "address": "Ons Dorp 1"
        }

    response = client.post(
        "/create-customer-auto-increment/",
        json=data)

    assert response.status_code == 200
    assert response.json() == data
    assert client.get((f"/get-customer-by-name/{data['lastName']}")).json() == data


def test_update_customer_address():
    data = {"address": "Ons Dorp 100"}

    response = client.put(
        "/update-customer-address/1", json=data)
    assert response.status_code == 200
    assert response.json()['address'] == data["address"]
    assert client.get(
        "/get-customer/1").json()['address'] == data["address"]


def test_update_customer_address_by_name():
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "address": "Imaginary street 1"
        }

    response = client.put(
        "/update-customer-address-by-name/", json=data)

    assert response.status_code == 200
    assert response.json()['address'] == data["address"]
    assert client.get(
        "/get-customer/0").json()['address'] == data["address"]


def test_delete_customer():
    response = client.delete("/delete-customer/0")

    assert response.status_code == 200
    assert response.json() == {'Message': 'Customer 0 deleted successfully.'}
    assert 'Customer does not exists yet.' in client.get("/get-customer/0").json()


def test_delete_customer_by_name():
    data = {
        "firstName": "Jamie",
        "lastName": "Dean"
        }

    response = client.delete("/delete-customer-by-name/", json=data)
    assert response.status_code == 200
    assert response.json() == {'Message': 'Customer Jamie Dean deleted successfully.'}
    assert 'Customer does not exists yet.' in client.get("/get-customer/2").json()
