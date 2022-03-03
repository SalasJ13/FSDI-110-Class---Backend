from http import client
import pymongo
import certifi

mongo_url = "mongodb+srv://salasFSDI:admin1986@cluster0.ozo9j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())

db = client.get_database("backendReactStore")