from mib.dao.manager import Manager
from mib.utils import LOTTERY_CONSTRAINTS
from mib import db 
from mib.models import LotteryParticipant
class LotteryManager(Manager):
    
    @staticmethod
    def get_participants():
        list = db.session.query(LotteryParticipant).all()
        return list

    @staticmethod
    def add_participant(email: str = None, choice: int=None):
        if LotteryManager.is_participating(email=email):
            return False
        else:
            Manager.check_none(email=email,choice=choice)
            participant = LotteryParticipant(participant_email=email, choice=choice)
            Manager.create(participant=participant)

    @staticmethod
    def is_participating(email: str) -> bool:
        Manager.check_none(email=email)
        return LotteryManager.get_participant(email=email) is not None

    @staticmethod
    def get_participant(email: str) -> LotteryParticipant:
        Manager.check_none(email=email)
        participant = (
            db.session.query(LotteryParticipant)
            .filter(LotteryParticipant.participant_email == email)
            .first()
        )
        return participant
    
    @staticmethod
    def change_choice(email: str, new_choice: int):
        Manager.check_none(email=email, new_choice=new_choice)
        p = LotteryManager.get_participant(email=email)
        p.choice = new_choice
        Manager.update()

    def remove_participant(email: str):
        p = LotteryManager.get_participant(email=email)
        Manager.delete(p=p)

    @staticmethod
    def reset_lottery() -> None:
        db.session.query(LotteryParticipant).delete()
        db.session.commit()