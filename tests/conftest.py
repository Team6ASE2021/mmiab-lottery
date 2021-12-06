import mock
import pytest

from mib import create_app
from mib import db
from mib.models.lottery_participant import LotteryParticipant


@pytest.fixture(scope="session", autouse=True)
def test_client():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_gp():
    with mock.patch("mib.dao.lottery_manager.LotteryManager.get_participant") as m:
        yield m


@pytest.fixture
def mock_ap():
    with mock.patch("mib.dao.lottery_manager.LotteryManager.add_participant") as m:
        yield m


@pytest.fixture
def participants():
    p1 = LotteryParticipant(participant_id=1, choice=2)
    p2 = LotteryParticipant(participant_id=2, choice=15)
    p3 = LotteryParticipant(participant_id=3, choice=50)
    db.session.add_all([p1, p2, p3])
    db.session.commit()
    yield p1, p2, p3
    db.session.delete(p1)
    db.session.delete(p2)
    db.session.delete(p3)
    db.session.commit()
