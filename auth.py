import jwt
import bcrypt

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET")

def hash_password(plain:str)->str:
    # we will change plain text to hashed text i.e cipher text
    salt=bcrypt.gensalt() #to prevent from rainbow attacks
    hashed_password=bcrypt.hashpw(plain.encode("utf-8"),salt).decode("utf-8")
    return hashed_password

def verify_password(plain:str,hashed:str)->bool:
    # to check plain text hash to the bcryp hash
    verify=bcrypt.checkpw(plain.encode("utf-8"),hashed.encode("utf-8"))
    return verify

