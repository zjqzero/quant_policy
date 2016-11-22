from pymongo import MongoClient

host = '172.17.0.2'
port = 27017

client = MongoClient(host, port)
