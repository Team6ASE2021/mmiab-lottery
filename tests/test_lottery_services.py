import pytest
from werkzeug.wrappers import response
from mib.dao.lottery_manager import LotteryManager
from mib.utils import LOTTERY_CONSTRAINTS,next_lottery_date
class TestLotteryServices:

    def test_get_lottery(self, test_client, participants):
        resp = test_client.get("/lottery")
        date = resp.json["date"]
        list_p = resp.json["participants"]
        assert date == next_lottery_date().strftime("%d/%m/%Y")
        assert len(list_p) == len(participants)
    
    def test_participate(self, test_client, mock_ap):
        json = {
            "email": "email@email.com",
            "choice":5}
        mock_ap.return_value = True
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.status_code == 201
        assert resp.json["status"] == "success"
        assert resp.json["message"] == "Participant successfully added"

    def test_participate_not_unique_email(self, test_client, mock_ap):
        json = {
            "email": "email@email.com",
            "choice":5}
        mock_ap.return_value = False
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.status_code == 200
        assert resp.json["status"] == "failure"
        assert resp.json["message"] == "A participant with the given email already exists"
    
    @pytest.mark.parametrize("bad_choice",[-1,-300,0,51,1000])
    def test_participate_bad_choice(self, test_client, mock_ap, bad_choice):
        json = {
                "email": "email@email.com",
                "choice":bad_choice}
        min = LOTTERY_CONSTRAINTS['min_choice']
        max = LOTTERY_CONSTRAINTS['max_choice']
        mock_ap.side_effect = ValueError(f"choice must be between {min} and {max}")
        resp = test_client.put("/lottery/participate",json=json)
        assert resp.status_code == 400