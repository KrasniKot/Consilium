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

        self.luqac = self.load_json_dataset('./data_extraction/data/luqac.jsonl')
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
    
    def paraphrase_one(self, sentence):
        """ Returns 3 paraphrases for a given sentece """
        # Load BART model and tokenizer
        model_name = "facebook/bart-large"
        bart_model = BartForConditionalGeneration.from_pretrained(model_name)
        model_tser = BartTokenizer.from_pretrained(model_name)

        # Encode input text
        input_ids = model_tser.encode(sentence, return_tensors="pt", truncation=True, padding=True)

        # Generate paraphrase
        output = bart_model.generate(
            input_ids, 
            num_beams=5, 
            num_return_sequences=3, 
            no_repeat_ngram_size=2,
            temperature=1.0,  # Increase creativity
            top_k=50,         # Control diversity of output
        )

        # Decode generated paraphrases
        paraphrases = [model_tser.decode(o, skip_special_tokens=True) for o in output]

        # Return the generated paraphrases
        return {paraphrase for paraphrase in paraphrases}

    def tokenize_example(self, itext, label):
        """ Format further a single example and tokenize it
            - itext ..... input text for the model
            - label ..... expected output
        """
        # Load pre-trained BART tokenizer
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

        # Tokenize input and target (answer)
        model_inputs = tokenizer(itext, max_length=1024, truncation=True, padding="max_length")
        labels = tokenizer(label, max_length=512, truncation=True, padding="max_length")

        # Ensure the labels are correctly shifted for the decoder
        model_inputs['labels'] = labels['input_ids']

        return model_inputs
