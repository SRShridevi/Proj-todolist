from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal,get_db
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv


router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv()
SEC_KEY=os.getenv("SEC_KEY")
ALGO=os.getenv("ALGO")

bcrypt=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class Userreq(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/")
def createuser(userdatas: Userreq, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == userdatas.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    createusermodel = Users(
        username=userdatas.username,
        hashedpassword=bcrypt.hash(userdatas.password)
    )
    db.add(createusermodel)
    db.commit()
    return {"message": "User created successfully", "user_id": createusermodel.id}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=authuser(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")        
    token=createtoken(user.username,user.id)
    return {"access_token": token, "token_type": "bearer"}

def authuser(username: str, password: str, db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt.verify(password,user.hashedpassword):
        return False
    return user

def createtoken(username: str, user_id: int):
    encode = {"sub": username, "user_id": user_id}
    encoded_jwt = jwt.encode(encode,SEC_KEY,algorithm=ALGO)
    return encoded_jwt


def protected_route(token: str = Depends(oauth2bearer), db: Session = Depends(get_db)):
    username, user_id=decodetoken(token)
    user = db.query(Users).filter(Users.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return {"message": f"Welcome {username}!"}

def decodetoken(token: str):
    try:
        payloaddetails= jwt.decode(token, SEC_KEY, algorithms=[ALGO])
        username: str = payloaddetails.get("sub")
        user_id: int = payloaddetails.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        return username, user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")




