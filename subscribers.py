from logging import log
import logging
import redis
import json
from flask import current_app
from mib.events.channels import SUBSCRIBE_CHANNEL_USER_DELETE
from concurrent.futures import ThreadPoolExecutor
from mib.events.redis_setup import get_redis
from mib.events.callbacks import delete_participant
from mib.dao.lottery_manager import LotteryManager
from mib import create_app
class EventSubscribers: # pragma: no cover

    @classmethod
    def participant_deleter(cls, app):
        redis_c = get_redis(app)
        p = redis_c.pubsub()
        p.subscribe(SUBSCRIBE_CHANNEL_USER_DELETE)
        logging.info(f"subscribed on channel {SUBSCRIBE_CHANNEL_USER_DELETE}")
        for message in p.listen():
           delete_participant(message)
    


event_subscribers = [
    {"subscriber":EventSubscribers.participant_deleter}
]


def init_subscribers(): # pragma: no cover
    app = create_app()
    logging.info("setting up subscribers...")
    EventSubscribers.participant_deleter(app)
if __name__ == "__main__":# pragma: no cover
    raise SystemExit(init_subscribers())