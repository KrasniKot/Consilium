import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

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
dataset    = pssor.load_dataset() 
dataset    = LUQaC(dataset, tokenizer)
dataloader = DataLoader(dataset, batch_size=3, shuffle=True)

# Set up the optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Set model to training mode
print('\nStarting the training...')
model.train()

# Training loop
loss_values = []
x_values    = []
epochs      = 100
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

        # Store the loss value for plotting
        loss_values.append(loss.item())
        x_values.append(e + (b + 1) / len(dataloader))

        print(f'processed batch {b} of {len(dataloader)}- total in epoch: {(b + 1) / len(dataloader):.4f} - epoch: {e} of {epochs} - loss: {loss.item():.4f}', end='\r')

    if e % 5 == 0:
        model.save_pretrained('../../trained_model')      # After each 5 epochs, save model
        tokenizer.save_pretrained('../../trained_model')  # Save the tokenizer as well

    # Plot the loss across all epochs
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, loss_values, label='Loss', color='b')
    plt.title('Cross-Entropy Loss Progress')
    plt.xlabel('Epoch (with Batch Progress)')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # Save the plot as an image after each epoch
    plt.savefig(f'cross_entropy_loss_progress.png')  # Save the plot image
    plt.close()  # Close the plot to avoid memory issues

    print()
