import json
import os
from fastapi import FastAPI

"""
As done with all other assignments, after completion of all exercises please push this directory using Git.
Execution of 'git add .\Modules\M5_API\ ', then committing these changes and eventually pushing them will start the pre-written test code.
This code will test whether the APIs that you created conform to the asked functionality.
For a more detailed description about how to execute and review these tests, we ask you to return to either the (M3) SQL or (M4) ML course.
At the bottom of these notebooks all steps are discussed in great detail.
"""

app = FastAPI()
# dataPath = os.path.join(os.getcwd().split('datacademy_demo')[0], "datacademy_demo", "data", "M5_API", "customers.json")
dataPath = os.path.join("data", "M5_API", "customers.json")

with open(dataPath, 'rb') as jsonFile:
    customers = json.load(jsonFile)
    customers = {i: customers[str(i)] for i in range(len(customers.keys()))}

# API GET Request(s) ####
@app.get("/get-customer/{customerId}")
def get_customer(customerId: int):
    if customerId not in customers:
        return {"Error", "Customer does not exists yet."}
    return customers[customerId]


@app.get("/get-customer-by-name/{lastName}")
def get_customer_by_name(lastName: str):
    for customerId in customers:
        if customers[customerId]['lastName'] == lastName:
            return customers[customerId]

    return {"Error", f"Customer with last name: '{lastName}' does not exists"}


@app.get("/get-customers/")
def get_customers(skip: int = 0, limit: int = 3):
    return {i: customers[i] for i in range(skip, min(skip+limit, len(customers)))}


# API POST Request(s) ####
@app.post("/create-customer/{customerId}")
def create_customer(customerId: int, firstName: str, lastName: str, address: str):
    if customerId in customers:
        return {"Error", f"customerId already used, next id available is: {max(customers.keys())+1}."}
        
    if (customerId - max(customers.keys())) > 1:
        return {"Error", f"customerId do not fit neatly together, next id available is: {max(customers.keys())+1}."}

    customers[customerId] = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address
    }
    return customers[customerId]


@app.post("/create-customer-auto-increment/")
def create_customer_autoincrement(firstName: str, lastName: str, address: str):
    customerId = max(customers.keys()) + 1

    customers[customerId] = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address
    }
    return customers[customerId]


# API PUT Request(s) ####
@app.put("/update-customer-address/{customerId}")
def update_customer_address(customerId: int, address: str):
    if customerId not in customers:
        return {"Error", "Customer does not exists."}

    customers[customerId]['address'] = address
    return customers[customerId]


@app.put("/update-customer-address-by-name/")
def update_customer_address_by_name(firstName: str, lastName: str, address: str):
    for customerId in customers:
        if customers[customerId]['firstName'] == firstName and customers[customerId]['lastName'] == lastName:
            customers[customerId]['address'] = address

            return customers[customerId]


# API DELETE Request(s) ####
@app.delete("/delete-customer/{customerId}")
def delete_customer(customerId: int):
    if customerId not in customers:
        return {"Error", "Customer does not exists."}

    del customers[customerId]
    return {"Message": f"Customer {customerId} deleted successfully."}


@app.delete("/delete-customer-by-name/")
def delete_customer_by_name(firstName: str, lastName: str):
    foundCustomer = False
    for customer in customers:
        if customers[customer]['firstName'] == firstName and customers[customer]['lastName'] == lastName:
            foundCustomer = True
            del customers[customer]
            break

    if not foundCustomer:
        return {"Error": "The customer you are trying to delete does not exist."}
    else:
        return {"Message": f"Customer {firstName} {lastName} deleted successfully."}