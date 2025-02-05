from fastapi import FastAPI
from db import engine, Base
from route import routes  
from models import Users, Task 
from auth import router as auth_router 
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth_router)
app.include_router(routes)  
