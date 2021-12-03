import pytest
import  json
from flask import current_app as app
from mib.events.redis_setup import get_redis
from mib.events.callbacks import  delete_participant
from mib import db 
from mib.models import LotteryParticipant



class TestSubscribersCallbacks:
    
    def test__delete_participant(self):
        p1 = LotteryParticipant(participant_id=1,choice=2)
        db.session.add(p1)
        db.session.commit()
        payload = {"type":"message","data":json.dumps({"user_id":p1.participant_id})}
        delete_participant(payload)
        assert db.session.query(LotteryParticipant).filter(LotteryParticipant.participant_id == 1).first() == None
    
    def test_delete_participant_not_message_type(self):
        p1 = LotteryParticipant(participant_id=1,choice=2)
        db.session.add(p1)
        db.session.commit()
        payload = {"type":"foo","data":json.dumps({"user_id":p1.participant_id})}
        delete_participant(payload)
        assert db.session.query(LotteryParticipant).filter(LotteryParticipant.participant_id == 1).first().participant_id == 1
        db.session.delete(p1)