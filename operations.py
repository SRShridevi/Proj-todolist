from sqlalchemy.orm import Session 
from models import Task  
from fastapi import HTTPException

class Operations: 
    def __init__(self,db:Session):
        self.database_session: Session=db

    def createtask(self, taskname: str,status:str="Pending"):
        if not taskname:
            raise HTTPException(status_code=400,detail="Taskname can't be empty")
        if len(taskname)<3 or len(taskname)>70:
            raise HTTPException(status_code=400,detail="Taskname must be between 3 and 70 characters")
        if status not in["Pending", "InProgress", "Completed"]:
            raise HTTPException(status_code=400, detail="Status is invalid.Allowed statuses are 'Pending','InProgress','Completed' ")
        duplicatetasks= self.database_session.query(Task).filter(Task.taskname==taskname).first()
        if duplicatetasks:
            raise HTTPException(status_code=409, detail="Task already exists")
        current_ids={t.taskid for t in self.database_session.query(Task).all()}
        newtaskid=1
        while newtaskid in current_ids:
            newtaskid+=1
        task = Task(taskid=newtaskid, taskname=taskname, status=status)
        self.database_session.add(task)
        self.database_session.commit()
        return {"message":"Task created successfully","task_id":newtaskid}
    
    def gettask(self, taskid: int):
        task=self.database_session.query(Task).filter(Task.taskid==taskid).first()
        if task:
            return{"task_id":task.taskid,"taskname":task.taskname,"status":task.status}
        raise HTTPException(status_code=404, detail="Task not found")
    
    def get_all_tasks(self):
        tasks=self.database_session.query(Task).all() 
        if tasks:
            task_list=[]
            for task in tasks:
                task_list.append({"task_id":task.taskid,"taskname":task.taskname,"status":task.status})
            return task_list
        raise HTTPException(status_code=404, detail="No tasks to show")
    
    
    def updatetask(self,taskid:int,taskname:str=None, status:str=None):
        task=self.database_session.query(Task).filter(Task.taskid==taskid).first()
        if not task:
            raise HTTPException(status_code=404,detail="Task not found")
        if not taskname and not status:
            raise HTTPException(status_code=400,detail="At least one field must be provided to update the task")
        if status not in ["Pending", "InProgress", "Completed"]:
            raise HTTPException(status_code=400, detail="Not a valid status.Allowed statuses re 'Pending','InProgress','Completed'")
        if taskname:
            if taskname==task.taskname:
                raise HTTPException(status_code=409, detail="Old and new task names can't be the same") 
            taskduplication=self.database_session.query(Task).filter(Task.taskname == taskname).first()
            if taskduplication:
                raise HTTPException(status_code=409, detail="This task already exists")
            task.taskname = taskname 
        
        if status:
            task.status = status
        self.database_session.commit()
        return {"message":"Task updated successfully"}
        
            
            
    def deletetask(self,taskid:int):
        task=self.database_session.query(Task).filter(Task.taskid == taskid).first()
        if not task:
            raise HTTPException(status_code=404,detail="Task not found")
        self.database_session.delete(task)
        self.database_session.commit()
        return {"message": "Task deleted successfully"}




            
        