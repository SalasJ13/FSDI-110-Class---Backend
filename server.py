
from itertools import count
from math import prod
import re
from unittest import result
from flask import Flask, abort, request
from mock_data import catalog
from about_me import me
import json
import random
from flask_cors import CORS
from config import db
from bson import ObjectId

#Servidor/app
app = Flask("server")
CORS(app)


#Creacion de rutas.
@app.route("/", methods=["get"])
def home_page():
    return "Under construction!"

@app.route("/about")
def about_me():
    return"Page About"

@app.route("/myAddress")
def get_address():
    address = me["address"]
    return f"{address['street']} {address['city']} {address['state']}"

@app.route("/test")
def test():
    return"I'm a simple test"

#########################
#API ENDPOINT
#########################
@app.route("/api/catalog")
def get_catalog():

    cursor=db.products.find({})
    results=[]
    for prod in cursor:
        prod["id"] = str(prod["_id"])
        prod["_id"] = ""
        results.append(prod)
    
    return json.dumps(results)




@app.route("/api/catalog", methods=["POST"])
def save_product():
#leer the payload as a dictionary frim json string
    product= request.get_json()

#VALDACIONES
#mostrar que el titulo tenga mas de 5 caracteres
    if not "title" in product or len(product["title"])<5:
        return abort(400, "There should be a title. Title should be least 5 chars long")
#Agregar el precio de manera obligatoria
    if not "price" in product:
        return abort(400,"Price is required")
#el precio no esta en enteros o decimal muestra un error 
    if not isinstance(product["price"],int) and not isinstance(product["price"],float):
        return abort(400,"Price es invalid")
#el precio debe ser mayor a cero
    if product["price"]<= 0:
        return abort(400,"Price should be grester than zero")
    
    db.products.insert_one(product)

    product["id"] = str(product["_id"])
    product["_id"] = ""
    
    return json.dumps(product)
#asignar un valor a id
    #product["id"]=random.randint(10000,50000)
    #catalog.append(product)#Guardar el valor de id
    #return json.dumps(product)



#con la funcion get(en Thunder Client) /api/catalog/count y regresar el num total de los productos
@app.route("/api/catalog/count")
def get_count():
    #count=len(catalog)
    #return json.dumps(count)
    cursor=db.products.find({})
    count=0
    for prod in cursor:
        count+=1
    
    json.dumps(count)

#con la funcion get(en Thunder Client) /api/catalog/sum y regresar el total de los precios de los productos
@app.route("/api/catalog/total")
def get_total():
    total=0
    for i in catalog:
        total+= i["price"] 
    res = f"${total}"
    return json.dumps(total)

#con la funcion get(en Thunder Client) /api/catalog/<id> buscar el producto desde el id 
@app.route("/api/product/<id>")
def get_product(id):

    if not ObjectId.is_valid(id):
        return abort(400,"id doesnt exist")

    prod=db.products.find_one({"id": ObjectId(id) })

    if not prod:
        return abort(400,"Product doesnt exist")

    prod["id"] = str(prod["_id"])
    prod["_id"] = ""
    return json.dumps(prod)
    #for i in catalog:
    #    if(id==i["id"]):
    #        return json.dumps(i)    
    #return abort(404)

#con la funcion get(en Thunder Client) /api/catalog/most_expensive y mostrar el producto mas caro
#
@app.route("/api/product/most_expensive")
def get_most_expensive():
    cursor=db.products.find({})
    pivot = catalog[0]
    for i in catalog:
        if i["price"] > pivot["price"]  :
            pivot=i
            
    return json.dumps(pivot)    

#Mostrar los resultado guardados de la variable category del metodo Catalog
@app.route("/api/categories")
def get_categories():
    cursor=db.products.find({})
    res=[]
    for i in cursor:
        category=i["category"]

        if not category in res:
            res.append(category)

    return json.dumps(res)

#crear una funcion que permita al cliente (reaccionar) recuperar todos los productos que pertenecen a la categoría específica
#el cliente enviará la categoría y esperará una lista de productos a cambio
@app.route("/api/catalog/<category>")
def get_products_category(category):
    res=[]
    cursor=db.products.find({"category":category})
    
    for prod in cursor:
        prod["id"] = str(prod["_id"])
        prod["_id"] = ""
        res.append(prod)
    return json.dumps(res)

############################
#API Methods for coupom codes
############################
coupons=[
    {
        "code":"Prueba"
    },
    {
        "code":"Prueba1"
    },
    {
        "code":"Prueba2"
    }

]
#Clase 3
@app.route("/api/coupons")
def get_coupons():
    cursor=db.coupons.find({})
    res=[]
    for prod in cursor:
        prod["id"] = str(prod["_id"])
        prod["_id"] = ""
        res.append(prod)
    return json.dumps(res)

@app.route("/api/coupons", methods=["POST"])
def save_coupons():
    coupon =request.get_json()
    #validacion
    db.coupons.insert_one(coupon)
    
    coupon["id"] = str(coupon["_id"])
    coupon["_id"] = ""

    return json.dumps(coupon)

@app.route("/api/coupons/<code>")
def get_coupon_code(code):
    coupon=db.coupons.find_one({"code":code})
    if not coupon:
        return abort(400,"Coupons doesnt exit" + code)
    coupon["id"] = str(coupon["_id"])
    coupon["_id"] = ""
    return json.dumps(coupon)

@app.route("/api/orders", methods=["POST"])
def get_save_order_products():

    order=request.get_json()#para insertar datos desde Thunder
    db.orders.insert_one(order)
    order["id"] = str(order["_id"])
    order["_id"] = ""
    return json.dumps(order)
#revisar esta cosa antes de enviarlo
@app.route("/api/orders/<user_id>")
def get_order_code(user_id):
    cursor=db.orders.find_one({"user_id":int(user_id) })
    res=[]
    for order in cursor:
        order["id"] = str(order["_id"])
        order["_id"] = ""
        res.append(order)
    return json.dumps(res)
            
#Iniciar el servidor
app.run(debug=True)
