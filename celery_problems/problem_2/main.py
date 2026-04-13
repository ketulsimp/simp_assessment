from tasks import send_email

task_1 = send_email.apply_async(args=["xyz@gmail.com"])