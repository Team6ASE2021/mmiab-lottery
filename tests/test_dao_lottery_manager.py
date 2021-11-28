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
        assert LotteryManager.add_participant(id=1, choice=3)
        p = LotteryParticipant.query.get(1)
        assert p.participant_id == 1
        assert p.choice == 3
        db.session.delete(p)
        db.session.commit()

    @pytest.mark.parametrize("id",[1,2,3])
    def test_add_participant_already_exists(self,participants,id):
        assert not LotteryManager.add_participant(id=id, choice=3)
    
    @pytest.mark.parametrize("id, expected",[ 
        (15, False),
        (1, True)
    ])
    def test_is_participating(self, participants, id, expected):
        assert LotteryManager.is_participating(id=id) == expected
    

    def test_get_participant_not_playing(self):
        p = LotteryManager.get_participant(id=13)
        assert p is None

    @pytest.mark.parametrize("id, expected",[ 
        (1, 2),
        (2, 15),
        (3, 50)
    ])
    def test_get_participant(self, participants, id, expected):
        p = LotteryManager.get_participant(id=id)
        assert p.choice == expected
    
    def test_remove_participant(self):
        p = LotteryParticipant(participant_id=1,choice=34)
        db.session.add(p)
        assert len(db.session.query(LotteryParticipant).all()) == 1
        LotteryManager.remove_participant(id=1)
        assert len(db.session.query(LotteryParticipant).all()) == 0

    def test_reset_lottery(self):
        p1 = LotteryParticipant(participant_id=1,choice=2)
        p2 = LotteryParticipant(participant_id=2, choice = 15)
        p3 = LotteryParticipant(participant_id=3, choice = 50)
        db.session.add_all([p1,p2,p3])
        assert len(db.session.query(LotteryParticipant).all()) == 3
        LotteryManager.reset_lottery()
        assert len(db.session.query(LotteryParticipant).all()) == 0
