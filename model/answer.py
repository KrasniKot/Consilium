import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("../../trained_model")
tokenizer = GPT2Tokenizer.from_pretrained("../../trained_model")
model.eval()

# Function to ask a question and get an answer
def ask_question(question):
    input_ids = tokenizer.encode(f'Question: {question} Answer:', return_tensors="pt")
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=512,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )

    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    print('-' * 30)
    return answer.split("Answer:")[-1].strip()  # Return the generated answer

# Example questions
print(ask_question('What the Article 332 mean?'))
print(ask_question('What can you tell me about the article 2 of the Uruguayan Constitution?'))
print(ask_question('Can I be arrested if caught committing a crime?'))