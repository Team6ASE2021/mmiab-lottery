import logging
import os
import random

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from mib.dao.lottery_manager import LotteryManager
from mib.events.publishers import EventPublishers

_APP = None

# BACKEND = "redis://localhost:6379"
# BROKER = "redis://localhost:6379/0"
CELERY_REDIS_HOST = os.getenv("CELERY_REDIS_HOST", "localhost")
CELERY_REDIS_PORT = os.getenv("CELERY_REDIS_PORT", 6379)
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB", 0)

BACKEND = f"redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}"
BROKER = f"redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/{CELERY_REDIS_DB}"
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

TaskBase = celery.Task


class ContextTask(TaskBase):  # pragma: no cover
    def __call__(self, *args, **kwargs):
        global _APP
        # lazy init
        if _APP is None:
            from mib import create_app

            app = _APP = create_app()

        else:
            app = _APP
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask
celery.conf.timezone = "Europe/Rome"
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
    json = {"users": [{"id": w, "points": 1} for w in winners]}
    EventPublishers.publish_lottery_winners(json)
    logger.log(logging.INFO, "Cleaning up lottery participants...")

    LotteryManager.reset_lottery()
    logger.log(logging.INFO, "Table reset done, waiting for next lottery")
    return json
