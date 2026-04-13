from celery_worker import celery_app
from tasks import daily_task, generate_daily_report, notify_user


app=celery_app()

@app.post('/run-daily-task')
def run_daily_task():
    daily_task.delay()
    return {"message":"Daily task has been scheduled"}

@app.post('/generate-report')
def generate_report(report_type:str,user_id:int):
    generate_daily_report.delay(report_type,user_id)
    return {"message":f"{report_type} report generation has been scheduled for user {user_id}"} 

@app.post('/notify-user')
def notify_user(user_id:int,message:str):
    notify_user.delay(user_id,message)
    return {"message":f"Notification has been scheduled for user {user_id} with message: {message}"}    


@app.get('/status')
def check_status(task_id:str):
    task_result=celery_app.AsyncResult(task_id,app=celery_app())
    return {"task_id":task_id,"status":task_result.status,"result":task_result.result}  

if __name__ == '__main__':
    app.run(debug=True)