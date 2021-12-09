from mib import db
from mib.dao.manager import Manager
from mib.models.lottery_participant import LotteryParticipant


class LotteryManager(Manager):
    """
    Wrapper class  for all db operations involving lottery
    """

    @staticmethod
    def get_participants():
        list = db.session.query(LotteryParticipant).all()
        return list

    @staticmethod
    def add_participant(id: int = None, choice: int = None):
        if LotteryManager.is_participating(id=id):
            return False
        else:
            Manager.check_none(id=id, choice=choice)
            participant = LotteryParticipant(participant_id=id, choice=choice)
            Manager.create(participant=participant)
            return True

    @staticmethod
    def is_participating(id: int) -> bool:
        Manager.check_none(id=id)
        return LotteryManager.get_participant(id=id) is not None

    @staticmethod
    def get_participant(id: int) -> LotteryParticipant:
        Manager.check_none(id=id)
        participant = (
            db.session.query(LotteryParticipant)
            .filter(LotteryParticipant.participant_id == id)
            .first()
        )
        return participant

    @staticmethod
    def remove_participant(id: int):
        p = LotteryManager.get_participant(id=id)
        if p is not None:
            Manager.delete(p=p)

    @staticmethod
    def reset_lottery() -> None:
        db.session.query(LotteryParticipant).delete()
        db.session.commit()
