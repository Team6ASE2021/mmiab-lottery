import mock
from mib import db 
from mib.models import LotteryParticipant
from mib.background import _lottery_draw

class TestLotteryDraw:

    def test_lottery_draw(self,test_client):
        p1 = LotteryParticipant(participant_id=1,choice=2)
        p2 = LotteryParticipant(participant_id=2, choice = 15)
        p3 = LotteryParticipant(participant_id=3, choice = 50)
        db.session.add_all([p1,p2,p3])
        db.session.commit()
        with mock.patch("random.randint") as m:
            m.return_value = 15 
            j = _lottery_draw()
            assert len(j["users"]) == 1
            assert len(db.session.query(LotteryParticipant).all()) == 0