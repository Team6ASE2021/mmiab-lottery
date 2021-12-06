import os
import logging
import random
import requests
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from mib.dao.lottery_manager import LotteryManager

_APP = None

# BACKEND = "redis://localhost:6379"
# BROKER = "redis://localhost:6379/0"
BACKEND = "redis://rd01:6379"
BROKER = "redis://rd01:6379/0"  
USERS = None
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

TaskBase = celery.Task


class ContextTask(TaskBase):  # pragma: no cover
    def __call__(self, *args, **kwargs):
        global _APP
        global USERS
        # lazy init
        if _APP is None:
            from mib import create_app

            app = _APP = create_app()
            USERS = _APP.config['USERS_MS_URL']
        else:
            app = _APP
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask

celery.conf.beat_schedule = {
    "lottery_draw": {
        "task": __name__ + ".lottery_draw",
        "schedule": crontab(0, 0, day_of_month=1),
    },
}

logger = get_task_logger(__name__)




@celery.task
def lottery_draw():
    """
    we use a helper function to decouple the draw from the celery decorator,
    this facilitate testing the function itself
    """
    _lottery_draw()  # pragma: no cover


def _lottery_draw():
    """
    The lottery simply chooses a number between 1 and 50 and assign one point to each user that correctly guessed
    the number.
    """
    logger.log(logging.INFO, "Drawing next lottery winners...")
    winner = random.randint(1, 50)
    logger.log(logging.INFO, f"Winning number: {winner}")

    participants = LotteryManager.get_participants()
    winners = list(
        map(
            lambda u: u.participant_id,
            filter(lambda u: u.choice == winner, participants),
        )
    )

    logger.log(logging.INFO, "Adding points to winners...")
    json = {
        [{
            "id":w,
            "points":1
        } for w in winners]
    }
    requests.post(f"{USERS}/lottery_update", json=json)

    logger.log(logging.INFO, "Cleaning up lottery participants...")

    LotteryManager.reset_lottery()
    logger.log(logging.INFO, "Table reset done, waiting for next lottery")
