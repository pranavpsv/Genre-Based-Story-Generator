from transformers import pipeline
from fastapi import FastAPI

app = FastAPI()

generate_story = pipeline("text-generation", "pranavpsv/gpt2-genre-story-generator")
from pydantic import BaseModel

class Item(BaseModel):
    prompt: str
    length: int

@app.post("/generate")
def generate(item: Item):
    prompt_text = item.prompt
    max_length = item.length
    return generate_story(prompt_text, max_length=max_length)


