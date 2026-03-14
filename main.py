from fastapi import FastAPI,Depends
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel

from sqlalchemy.orm import Session
from database import engine,get_db
from models import Base,QueryLog,Users
from uuid import UUID

from components import UserOut

import bcrypt
import os

load_dotenv()

GROQ_API=os.getenv("GROQ_API_KEY")

Base.metadata.create_all(bind=engine) #to create table at start

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
def ask(data: AskQuestion, db: Session = Depends(get_db)):
    question = data.question

    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question}
        ],
        model=model
    )
    answer = response.choices[0].message.content

    log = QueryLog(question=question, response=answer)
    db.add(log)
    db.commit()

    return {"answer": answer}

@app.get('/history')
def get_history(db:Session=Depends(get_db)):
    logs=db.query(QueryLog).order_by(QueryLog.created_at.desc()).all()

    return [{"question": l.question, "response": l.response, "time": l.created_at} for l in logs]

@app.post("/register")
def regester(username:str,password=str, db: Session=Depends(get_db)):
    hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    user=Users(username=username,password=hashed)
    db.add(user)
    db.commit()

    return f"User Regestered Succlessfully"


@app.get("/users", response_model=list[UserOut])
def get_user(db:Session=Depends(get_db)):
    users=db.query(Users.id,Users.username).order_by(Users.username.asc()).all()
    return users