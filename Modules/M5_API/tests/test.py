from Modules.M5_API.src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


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

    response = client.post("/create-customer/12?firstName=Jan&lastName=Janssen&address=Kerkstraat%2010")
    
    assert response.status_code == 200
    assert response.json() == data


def test_create_customer_auto_increment():
    response = client.get("/get-customers/?skip=0&limit=1000")
    keys_customers = list(response.json().keys())
    
    assert response.status_code == 200
    assert (int(keys_customers[-1]) - int(keys_customers[-2])) == 1


def test_update_customer_address():
    data = {"address": "Ons Dorp 100"}

    response = client.put("/update-customer-address/1?address=Ons%20Dorp%20100")
    assert response.status_code == 200
    assert response.json()['address'] == data["address"]
    assert client.get("/get-customer/1").json()['address'] == data["address"]


def test_update_customer_address_by_name():
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "address": "Imaginary street 1"
        }

    response = client.put("/update-customer-address-by-name/?firstName=John&lastName=Doe&address=Imaginary%20street%201")

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
    response = client.delete("/delete-customer-by-name/?firstName=Jamie&lastName=Dean")
    
    assert response.status_code == 200
    assert response.json() == {'Message': 'Customer Jamie Dean deleted successfully.'}
    assert 'Customer does not exists yet.' in client.get("/get-customer/2").json()
