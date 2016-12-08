import os
from pymongo import MongoClient

host = os.environ.get('MONGO_DB_ADDR') or '127.0.0.1'
port = os.environ.get('MONGO_DB_PORT') or 6060

client = MongoClient(host, int(port))
