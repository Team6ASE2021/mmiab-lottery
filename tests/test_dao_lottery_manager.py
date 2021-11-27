import pytest

from mib.dao.lottery_manager import LotteryManager
from mib import db
from mib.models.lottery_participant import LotteryParticipant
class TestLotteryManager:
    
    
    def test_get_participants_empty(self):
        ps = LotteryManager.get_participants()
        assert len(ps) == 0

    def test_get_participants(self, participants):
        ps = LotteryManager.get_participants()
        assert len(ps) == 3

    def test_add_participant_no_fields(self):
        with pytest.raises(ValueError):
            LotteryManager.add_participant()
    
    def test_add_participant(self):
        LotteryManager.add_participant(email="email@email.com", choice=3)
        p = LotteryParticipant.query.get(1)
        assert p.participant_email == "email@email.com"
        assert p.choice == 3
        db.session.delete(p)
        db.session.commit()

    def test_add_participant_already_exists(self,participants):
        assert not LotteryManager.add_participant(email="email@email.com", choice=3)
    
    @pytest.mark.parametrize("email, expected",[ 
        ("fail@fail.com", False),
        ("email@email.com", True)
    ])
    def test_is_participating(self, participants, email, expected):
        assert LotteryManager.is_participating(email=email) == expected
    

    def test_get_participant_not_playing(self):
        p = LotteryManager.get_participant(email="email@email.com")
        assert p is None
    @pytest.mark.parametrize("email, expected",[ 
        ("email@email.com", 2),
        ("email2@email2.com", 15),
        ("email3@email3.com", 50)
    ])
    def test_get_participant(self, participants, email, expected):
        p = LotteryManager.get_participant(email=email)
        assert p.choice == expected
    
    @pytest.mark.parametrize("email,old, new",[ 
        ("email@email.com", 2,13),
        ("email2@email2.com", 15,12),
        ("email3@email3.com", 50,1)
    ])
    def test_update_choice(self, participants, email, old, new):
        p = LotteryManager.get_participant(email=email)
        assert p.choice == old 
        LotteryManager.change_choice(email=email, new_choice=new)
        assert p.choice == new
    
    def test_remove_participant(self):
        p = LotteryParticipant(participant_email="email@email.com",choice=34)
        db.session.add(p)
        assert len(db.session.query(LotteryParticipant).all()) == 1
        LotteryManager.remove_participant(email = p.participant_email)
        assert len(db.session.query(LotteryParticipant).all()) == 0

    def test_reset_lottery(self):
        p1 = LotteryParticipant(participant_email="email@email.com",choice=2)
        p2 = LotteryParticipant(participant_email="email2@email2.com", choice = 15)
        p3 = LotteryParticipant(participant_email="email3@email3.com", choice = 50)
        db.session.add_all([p1,p2,p3])
        assert len(db.session.query(LotteryParticipant).all()) == 3
        LotteryManager.reset_lottery()
        assert len(db.session.query(LotteryParticipant).all()) == 0
