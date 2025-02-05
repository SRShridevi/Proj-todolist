from sqlalchemy import Column, Integer, String
from db import Base
class Task(Base):
    __tablename__="tasks"
    taskid=Column(Integer, primary_key=True, index=True)  
    taskname=Column(String, index=True)  
    status=Column(String, default="Pending") 
    user_id = Column(Integer) 

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, unique=True, nullable=False, index=True)  
    hashedpassword = Column(String, nullable=False)  
