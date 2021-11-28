import pytest
from mib.models.lottery_participant import LotteryParticipant
from mib.utils import next_lottery_date
from mib import db
class TestLotteryServices:

    def test_get_lottery(self, test_client, participants):
        resp = test_client.get("/lottery")
        date = resp.json["date"]
        list_p = resp.json["participants"]
        assert date == next_lottery_date().strftime("%d/%m/%Y")
        assert len(list_p) == len(participants)
    
    def test_participate(self, test_client, mock_ap):
        json = {
            "id":1,
            "choice":5}
        mock_ap.return_value = True
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.status_code == 201
        assert resp.json["status"] == "success"
        assert resp.json["message"] == "Participant successfully added"

    def test_participate_not_unique_id(self, test_client, mock_ap):
        json = {
            "id":1,
            "choice":5}
        mock_ap.return_value = False
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.status_code == 200
        assert resp.json["status"] == "failure"
        assert resp.json["message"] == "A participant with the given email already exists"
    
    @pytest.mark.parametrize("bad_choice",[-1,-300,0,51,1000])
    def test_participate_bad_choice(self, test_client, mock_ap, bad_choice):
        json = {
                "id":1,
                "choice":bad_choice}
        mock_ap.side_effect = ValueError()
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.json["title"] == "Bad Request"
        assert resp.status_code == 400
    
    @pytest.mark.parametrize("id, choice", [
        (1,2),
        (2,15),
        (3,50)])
    def test_get_choice(self, test_client, participants, id, choice):
        resp = test_client.get(f"/lottery/{id}")
        assert resp.json["choice"] == choice
        assert resp.status_code == 200 
    
    @pytest.mark.parametrize("id", [0,223,55,340])
    def test_get_choice_user_not_found(self, test_client, participants,id):
        resp = test_client.get(f"/lottery/{id}")
        assert resp.json["message"] == "No user with the given participant id found"
        assert resp.status_code == 404
    

    @pytest.mark.parametrize("id", [4,15])
    def test_remove_participant(self, test_client,participants,id ):
        p = LotteryParticipant(participant_id=4,choice=2)
        db.session.add(p)
        db.session.commit()
        resp = test_client.delete(f"/lottery/{id}")
        assert resp.json["message"] == "Participant successfully deleted"
        assert resp.status_code == 200