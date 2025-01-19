import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader

from preprocess_data import Preprocessor

# Define the LUQaC dataset
class LUQaC(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        tokenizer.pad_token = tokenizer.eos_token  # Set padding token to EOS
        self.encodings      = tokenizer(texts, padding=True, truncation=True, max_length=max_length)

    def __len__(self):
        return len(self.encodings['input_ids'])

    def __getitem__(self, idx):
        return {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}

# Load pretrained GPT-2 model and tokenizer
print('\nLoading pretrained model...')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model     = GPT2LMHeadModel.from_pretrained('gpt2')

# Build the dataset instance
print('\nBuilding dataset...')
pssor      = Preprocessor()
dataset = ("What does it mean the Article 332 found in the Constitution?", "Article 332 means that the provisions of the Constitution that recognize rights for individuals, as well as those that grant powers and impose duties on public authorities, will not cease to be applied due to the lack of specific regulations. Instead, they will be supplemented by analogous laws, general principles of law, and widely accepted doctrines.")
dataset    = LUQaC([dataset], tokenizer)
dataloader = DataLoader(dataset, batch_size=2)

# Set up the optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Set model to training mode
print('\nStarting the training...')
model.train()

# Training loop
epochs = 100
for e in range(epochs):
    for b, batch in enumerate(dataloader):

        input_ids      = batch["input_ids"]
        attention_mask = batch["attention_mask"]

        optimizer.zero_grad()  # Zero the gradients

        # Forward pass
        outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
        loss    = outputs.loss

        loss.backward()   # Backward pass
        optimizer.step()  # Update weights

        print(f'processed batch {b} - total in epoch: {(b + 1) / len(dataloader):.4f} - epoch: {e} - loss: {loss.item():.4f}', end='\r')

    if e % 5 == 0:
        model.save_pretrained('../../trained_model')     # After each 5 epochs, save model
        tokenizer.save_pretrained('../../trained_model')  # Save the tokenizer as well
    print()
