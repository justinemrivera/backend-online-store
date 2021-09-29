import pymongo

# connection string
# external server # mongo_url = "mongodb+srv://.........."
# free service: mongodb.net

# localhost
mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)
# db points to the actual data base
db = client.get_database("onlineStore")
