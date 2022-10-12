import json
import os
from typing import Dict
from fastapi import FastAPI

app = FastAPI()
dataPath = os.path.join(os.getcwd().split('datacademy_demo')[0], "datacademy_demo", "data", "M5_API", "customers.json")

with open(dataPath, 'rb') as jsonFile:
    customers = json.load(jsonFile)
    customers = {i: customers[str(i)] for i in range(len(customers.keys()))}



### API GET Request(s) ####
@app.get("/get-customer/{customerId}")
def get_customer(customerId: int) -> dict:
    if customerId not in customers:
        return {"Error", "Customer does not exists yet."}
    return customers[customerId]


# @app.get("/get-customer-by-name/")
# def get_customer_by_name(lastName: str) -> dict:
#     #TODO: INSERT API CODE HERE.


# @app.get("/get-customers/")
# def get_customers(skip: int, limit: int) -> dict:
#     #TODO: INSERT API CODE HERE.





### API POST Request(s) ####
@app.post("/create-customer/{customerId}")
def create_customer(customerId: int, firstName: str, lastName: str, address: str) -> dict:
    if customerId in customers:
        return {"Error", f"customerId already used, next id available is: {max(customers.keys())+1}."}
    
    customers[customerId] = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address
    }
    return customers[customerId]


# @app.post("/create-customer-auto-increment/")
# def create_customer(firstName: str, lastName: str, address: str) -> dict:
#     #TODO: INSERT API CODE HERE.





### API PUT Request(s) ####
@app.put("/update-customer-address/{customerId}")
def update_customer_address(customerId: int, address: str) -> dict:
    if customerId not in customers:
        return {"Error", "Customer does not exists."}
    
    customers[customerId]['address'] = address
    return customers[customerId]


# @app.put("/update-customer-address-by-name/")
# def update_customer_address(firstName: str, lastName: str, address: str) -> dict:
#     #TODO: INSERT API CODE HERE.





### API DELETE Request(s) ####
@app.delete("/delete-customer/{customerId}")
def delete_customer(customerId:int) -> dict:
    if customerId not in customers:
        return {"Error", "Customer does not exists."}
    
    del customers[customerId]
    return {"Message": "Customer deleted successfully."}


# @app.delete("/delete-customer-by-name/")
# def delete_customer_by_name(firstName: str, lastName:str) -> dict:
#     #TODO: INSERT API CODE HERE.