from mib import db


class LotteryParticipant(db.Model):
    """Representation of LotteryParticipant model."""

    __tablename__ = "lottery_participant"
    SERIALIZE_LIST = ["participant_id", "choice"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_id = db.Column(db.Integer, unique=True)
    choice = db.Column(db.Integer, nullable=False)

    def serialize(self):
        _dict = dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
        return _dict
