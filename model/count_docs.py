from pymongo import MongoClient
import json
import random
from googletrans import Translator

from preprocess_data import Preprocessor

pssor = Preprocessor()
# Connect to your MongoDB instance
# Access the database
db = pssor.db

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

# Access the constitution_articles collection
collection = db['constitution_articles']

# Find the document with id
print(collection.find_one({"_id": 25}))  # Article 25 was included in the dataset

# Add template lines to the jsonl dataset from the 26th article on
translator = Translator()
with open('../../data/luqac.jsonl', 'a') as f, open('../../data/logs.txt', 'a') as logsf:
    for art in collection.find({'_id': {'$gt': 25}}):
        # Create the question
        q = f"{random.choice(['Can you explain', 'What does it mean'])} the Article {art['_id']} found in the {random.choice(['', 'Uruguayan '])}Constitution?"

        try:
            # Create the tranlsated context
            artnt = (art.get('CAPITULO') or '') + ' ' + (art.get('SECCION') or '') + ' ' + art['content']
            c = translator.translate(artnt.strip(), src='es', dest='en')

            # Add line to the jsonl dataset with the question and context and add answer later, manually
            json_line = json.dumps({'q': q, 'a': '', 'c': c.text})

            f.write(json_line + "\n")
            print('Article', art['_id'], 'added to jsonl dataset...', end='\r')

        except TypeError:
            logsf.write(f'Article {art["_id"]} could not be added successfully\n')
print()
