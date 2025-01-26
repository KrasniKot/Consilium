import random
import json

from pymongo import MongoClient


class Preprocessor:
    """ Defines a Preprocessor """

    def __init__(self):
        """ Initializes a Preprocessor Instance """
        self.client = MongoClient("mongodb://elated_pare:27017/")
        self.db     = self.client['laws_db']
        self.prrt   = None

        print('LUQaC dataset loaded...')

    def load_json_dataset(self, path):
        """ Loads a json dataset """
        self.set_parrot()

        collection = self.db['augmented_luqac']
    
        # Check if the collection exists, and clear it
        if collection.count_documents({}) > 0:
            print('Collection already exists, clearing it...\n')
            collection.delete_many({}) 

        # Open the JSONL file
        with open(path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                print(f'Reading line {i}...', end='\r')
                record = json.loads(line) # Parse each JSON line
                if record.get('a'):
                    self.save_aug_luqac(collection, (record.get('q'), record.get('a')))  # Add the raw question to the dataset
                    self.save_aug_luqac(collection, (self.apply_typos(record.get('q')), record.get('a')))  # Add same question with typos

                    for pq in self.paraphraseq(record.get('q')):  # Paraphrase the question
                        if pq.lower() not in record.get('q').lower():
                            self.save_aug_luqac(collection, (pq, record.get('a')))  # Convert to tuple format (question, answer)
                            self.save_aug_luqac(collection, (self.apply_typos(pq), record.get('a')))  # Add same paraphrased question with typos

        print(f"Augmented dataset with {collection.count_documents({})} examples has been saved to MongoDB.")

    def paraphraseq(self, question):
        """ Returns paraphrases for a question """
        paraphrases = self.prrt.augment(question)
        if paraphrases is None:
            return []  # Return an empty list if no paraphrases are found

        return {paraphrase[0] for paraphrase in paraphrases} 

    def simulate_typo(self, word):
        """ Simulate typos in a word, including swapping adjacent characters and occasionally removing a character. """
        # If the word is just one character long, return the word
        if len(word) < 2:
            return word

        # Define probabilities for different typo types
        remove_prob = 0.1  # 10% chance to remove a character

        # Decide the type of typo to simulate
        if random.random() < remove_prob:
            # Remove a random character
            index = random.randint(0, len(word) - 1)
            word  = word[:index] + word[index+1:]

        if len(word) > 1:
            index = random.randint(0, len(word) - 2)
            return word[:index] + word[index+1] + word[index] + word[index+2:]

        return word

    def apply_typos(self, sentence, typo_prob=0.38):
        """ Applies typos to all of the words given a sentence and a probability """
        # Split the sentence into a list of words
        words = sentence.split()

        # Apply tipos to a words if the generated number is lesser than the probability
        augmented_words = [self.simulate_typo(word) if random.random() < typo_prob else word for word in words]

        # Return the joined sentence
        return ' '.join(augmented_words)


    def save_aug_luqac(self, col, row):
        """ Saves the luqac dataset into a mongo db collection """
        # Insert the document into the MongoDB collection
        col.insert_one({'q': row[0], 'a': row[1]})

    def load_dataset(self):
        """ Loads the LUQaC dataset """
        collection = self.db['augmented_luqac']

        # Fetch all documents from the collection
        documents = collection.find()

        # Extract 'q' and 'a' fields and return as a list of tuples
        return  [(doc['q'], doc['a']) for doc in documents if 'q' in doc and 'a' in doc]

    def set_parrot(self):
        from parrot import Parrot
        self.prrt = Parrot()


if __name__ == '__main__':
    pssor = Preprocessor()  # Create an instance of the class
    pssor.luqac = pssor.load_json_dataset('../../data/luqac.jsonl')  # Load the dataset and augment it
