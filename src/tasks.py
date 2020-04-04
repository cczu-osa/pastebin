import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from src.app import app
from src.database import service


def schedule_task():
    with app.app_context():
        service.trim()


scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_task, trigger="interval", weeks=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
