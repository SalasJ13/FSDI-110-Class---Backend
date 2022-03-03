#declarar funcion
from cmath import pi
from email.headerregistry import Address


def name():
    print( "Jazmin Salas")

def test_dict():
    print("Dictonary")

    me={
        "first": "Jo",
        "last": "Salas",
        "age": 21,
        "hobbies": [],
        "address": {
            "street":"evergreen",
            "city":"Tijuana"
        }
    }

    print(me["first"]  +  " " +  me["last"])
    address=me["address"]
    print(address["street"]+" " + address["city"])

def younger_pers():
    ages = [12,42,32,50,56,14,78,30,51,89,12,38,67,10]
    pivot = ages[0]
    for i in ages:
        if(i<pivot):
            pivot=i
    print(f"Menor: " + {pivot})


name()
test_dict()
younger_pers()