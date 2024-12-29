from pymongo import MongoClient

# Connect to your MongoDB instance
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if needed

# Access the database
db = client['laws_db']

# Get a list of all collections in the database
collections = db.list_collection_names()

# Define the width for alignment
name_width = max(len(collection) for collection in collections) + 3  # Find the longest collection name

# Iterate over each collection and count the documents
for collection_name in collections:
    collection = db[collection_name]
    count = collection.count_documents({})
    # Print the collection name and count, aligned with padding
    print(f'Collection <{collection_name}> contains:', ' ' * (name_width - len(collection_name)), count)
