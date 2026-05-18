from celery import Celery
import os

def make_celery():
    return Celery("tasks", broker=os.environ["REDIS_URL"])

celery = make_celery()

@celery.task
def send_reminder(todo_title):
    print(f"Reminder: don't forget to '{todo_title}'! ")
    