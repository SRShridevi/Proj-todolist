from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from operations import Operations
from db import get_db

routes=APIRouter()

@routes.post("/tasks/")
def createtask(taskname:str,status:str="Pending",db:Session=Depends(get_db)):
    operations = Operations(db)
    return operations.createtask(taskname, status)
    
@routes.get("/tasks/{taskid}")
def gettask(taskid:int,db:Session=Depends(get_db)):
    operations = Operations(db)
    return operations.gettask(taskid)
    
@routes.get("/tasks/")
def get_all_tasks(db:Session=Depends(get_db)):
    operations = Operations(db)
    return operations.get_all_tasks()

@routes.put("/tasks/{taskid}")
def updatetask(taskid: int,taskname: str=None,status:str=None,db: Session=Depends(get_db)):
    operations = Operations(db)
    return operations.updatetask(taskid,taskname,status)

@routes.delete("/tasks/{taskid}")
def deletetask(taskid: int,db:Session=Depends(get_db)):
    operations = Operations(db)
    return operations.deletetask(taskid)