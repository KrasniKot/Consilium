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
            top_p=0.90,
            temperature=0.75
        )

    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    print('-' * 35, question)
    return answer.split("Answer:")[-1].strip()  # Return the generated answer


if __name__ == '__main__':
    # Example questions
    #print(ask_question('Explain article 196'))
    #print(ask_question('What can you tell me about the article 2 of the Uruguayan Constitution?'))
    #print(ask_question('Can I be arrested if caught committing a crime?'))
    print(ask_question('I do not understand the first article of the Constitution'))
    print(ask_question('So, can I take over the world?'))
    print(ask_question('Could yuo explain article 103 of Constitutioon?'))
    print(ask_question('Article 293'))
    print(ask_question('Supreme Court of Justice'))