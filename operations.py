from sqlalchemy.orm import Session
from models import Task
from fastapi import HTTPException

class Operations:
    def __init__(self,db:Session,user_id:int,username:str):
        self.database_session:Session=db
        self.user_id=user_id
        self.username=username

    def createtask(self,taskname:str,status:str="Pending"):
        if not taskname:
            raise HTTPException(status_code=400,detail="Taskname can't be empty")
        if len(taskname)<3 or len(taskname)>70:
            raise HTTPException(status_code=400,detail="Taskname must be between 3 and 70 characters")
        if status not in["Pending","InProgress","Completed"]:
            raise HTTPException(status_code=400,detail="Invalid status.Allowed: 'Pending','InProgress','Completed'")
        duplicatetasks=self.database_session.query(Task).filter(Task.taskname==taskname,Task.user_id==self.user_id).first()
        if duplicatetasks:
            raise HTTPException(status_code=409,detail="Task already exists")
        task=Task(taskname=taskname,status=status,user_id=self.user_id)
        self.database_session.add(task)
        self.database_session.commit()
        self.database_session.refresh(task)
        return {"message":"Task created successfully","task_id":task.taskid}

    def gettask(self,taskid:int):
        task=self.database_session.query(Task).filter(Task.taskid==taskid,Task.user_id==self.user_id).first()
        if task:
            return {"task_id":task.taskid,"taskname":task.taskname,"status":task.status}
        raise HTTPException(status_code=404,detail="Task not found")

    def get_all_tasks(self):
        tasks=self.database_session.query(Task).filter(Task.user_id==self.user_id).all()
        return [{"task_id":task.taskid,"taskname":task.taskname,"status":task.status} for task in tasks]

    def updatetask(self,taskid:int,taskname:str=None,status:str=None):
        if not (taskname or status):
            raise HTTPException(status_code=400, detail="At least one field must be provided to update the task")
        task = self.database_session.query(Task).filter_by(taskid=taskid, user_id=self.user_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if taskname and taskname!=task.taskname:
            if self.database_session.query(Task).filter_by(taskname=taskname, user_id=self.user_id).first():
                raise HTTPException(status_code=409,detail="This task already exists")
            task.taskname=taskname
        if status and status not in {"Pending", "InProgress", "Completed"}:
            raise HTTPException(status_code=400, detail="Invalid status. Allowed: 'Pending', 'InProgress', 'Completed'")
        task.status = status                      
        self.database_session.commit()
        return {"message": "Task updated successfully"}

    def deletetask(self,taskid:int):
        task=self.database_session.query(Task).filter(Task.taskid==taskid,Task.user_id==self.user_id).first()
        if not task:
            raise HTTPException(status_code=404,detail="Task not found")
        self.database_session.delete(task)
        self.database_session.commit()
        return {"message":"Task deleted successfully"}
