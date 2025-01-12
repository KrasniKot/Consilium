import random
import json

from pymongo import MongoClient
from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration


class Preprocessor:
    """ Defines a Preprocessor """

    def __init__(self):
        """ Initializes a Preprocessor Instance """
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db     = self.client['laws_db']

        self.luqac = self.load_json_dataset('../../data/luqac.jsonl')
        print('LUQaC dataset loaded...')

    def load_json_dataset(self, path):
        """ Loads a json dataset """
        examples = []

        # Open the JSONL file
        with open(path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                print(f'Reading line {i}...', end='\r')
                record = json.loads(line)  # Parse each JSON line
                examples.append((record["q"], record["a"]))  # Convert to tuple format (question, answer)

        print()
        return examples

    def paraphraseq(self, question):
        """ Returns paraphrases for a question """
        
