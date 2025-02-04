from fastapi import FastAPI
from db import engine, Base
from route import routes  
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routes)  