from fastapi import FastAPI, Depends, status, HTTPException
from groq import Groq
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, QueryLog, Users
from uuid import UUID

from components import UserOut, TokenData, TokenResponse, UserLogin, UserRegister, AskQuestion
from auth import hash_password, verify_password, create_access_token, get_current_user

import os

load_dotenv()

GROQ_API = os.getenv("GROQ_API_KEY")

Base.metadata.create_all(bind=engine)

app = FastAPI()
client = Groq(api_key=GROQ_API)
model = os.getenv("MODEL_NAME")


@app.get('/health')
def get_health():
    return {'status': "Healthy"}


@app.post('/ask')
def ask(
    data: AskQuestion,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
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
def get_history(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    logs = db.query(QueryLog).order_by(QueryLog.created_at.desc()).all()
    return [{"question": l.question, "response": l.response, "time": l.created_at} for l in logs]


@app.get("/users", response_model=list[UserOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    users = db.query(Users.id, Users.username,Users.email).order_by(Users.username.asc()).all()
    return users


@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.username == user.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    new_user = Users(
        username=user.username,
        password=hash_password(user.password),
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(id=new_user.id, username=new_user.username)


@app.post("/auth/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = create_access_token({"sub": db_user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")


@app.get("/dashboard")
def dashboard(current_user: TokenData = Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {current_user.username}!"}