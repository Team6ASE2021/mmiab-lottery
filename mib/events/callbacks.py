import json
import logging
from mib.dao.lottery_manager import LotteryManager
def delete_participant(message):
     if message["type"] == "message":
        usr = json.loads(message["data"])
        id  = usr.get("user_id")
        LotteryManager.remove_participant(id)
        logging.info(f"removed participant with user_id {id}")