import os
from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel

load_dotenv()

GROQ_API=os.getenv("GROQ_API_KEY")

app=FastAPI()
client=Groq(api_key=GROQ_API)
model="openai/gpt-oss-120b"
history=[]

@app.get('/health')
def get_health():
    return {'status':"Healthy"}

class AskQuestion(BaseModel):
    question:str


@app.post('/ask')
def ask(data:AskQuestion):
    question=data.question

    responce=client.chat.completions.create(
        messages=[
            {"role":"user","content":question}
        ],
        model=model
    )
    answer=responce.choices[0].message.content

    history.append({
        "question":question,
        "answer":answer
    })
    return{"answer":answer}

@app.get('/history')
def get_history():
    return history