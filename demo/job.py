from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)

scheduler = APScheduler()

# define your job function
def my_job():
    print('This is a job running in the background.')

# define your job function
def my_job_1():
    print('This is a job 1.')

# add the job to the scheduler
scheduler.add_job(id='my_job', func=my_job, trigger='interval', seconds=10)
scheduler.add_job(id='my_job_1', func=my_job_1, trigger='interval', seconds=20)

# start the scheduler
scheduler.start()

# run the Flask app
if __name__ == '__main__':
    app.run()
