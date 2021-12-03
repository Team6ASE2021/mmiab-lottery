from typing import Dict
import json
from flask import current_app
from mib.events.redis_setup import get_redis
from mib.events.channels import PUBLISH_CHANNEL_LOTTERY_WINNERS
class EventPublishers:


    @classmethod
    def publish_lottery_winners(self, msg: Dict):
        if "users" not in msg:
            return None
        else:
            return get_redis(current_app).publish(PUBLISH_CHANNEL_LOTTERY_WINNERS,json.dumps(msg))