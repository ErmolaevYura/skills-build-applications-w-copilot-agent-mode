from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['octofit_db']

# Fetch collections
collections = db.list_collection_names()
print("Collections:", collections)

# Fetch data from users collection
users = list(db['users'].find())
print("Users:", users)