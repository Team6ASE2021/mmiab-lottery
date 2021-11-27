from enum import unique
from mib import db
class LotteryParticipant(db.Model):
    # Table that stores the participants for the next lottery
    __tablename__ = "lottery_participant"
    SERIALIZE_LIST = ["participant_email", "choice"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_email = db.Column(db.Unicode(255), unique=True)
    choice = db.Column(db.Integer, nullable=False)
    
    def serialize(self):
        _dict = dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
        return _dict