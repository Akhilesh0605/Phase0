from pydantic import BaseModel,EmailStr

class UserOut(BaseModel):
    username: str
    email: str | None=None

    model_config = {"from_attributes": True}

class TokenData(BaseModel):
    username:str | None=None  

class UserRegister(BaseModel):
    username:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"

class AskQuestion(BaseModel):
    question: str