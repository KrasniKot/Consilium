from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Model imports
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Load the trained model and tokenizer
model      = GPT2LMHeadModel.from_pretrained("../../trained_model")
tokenizer  = GPT2Tokenizer.from_pretrained("../../trained_model")
model.eval()


# Serve static files
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/styles', StaticFiles(directory='styles'), name='styles')
app.mount('/scripts', StaticFiles(directory='scripts'), name='scripts')


# Main page
@app.get('/', response_class=HTMLResponse)
async def get_index():
    html_path = Path(__file__).parent / 'static' / 'index.html'
    with open(html_path, "r") as f:
        content = f.read()
    return content


class QuestionRequest(BaseModel):
    question: str


@app.post('/ask')
async def ask_question(request: QuestionRequest):
    """Answers a given question"""
    question       = request.question
    input_ids      = tokenizer.encode(f'Question: {question} Answer:', return_tensors="pt")
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
    return {"answer": answer.split("Answer:")[-1].strip()}