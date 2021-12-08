from flask import request
from flask.json import jsonify

from mib.dao.lottery_manager import LotteryManager
from mib.utils import next_lottery_date


def get_next_lottery():
    participants = LotteryManager.get_participants()
    date = next_lottery_date()
    return (
        jsonify(
            {
                "date": date.strftime("%d/%m/%Y"),
                "participants": [p.serialize() for p in participants],
            }
        ),
        200,
    )


def participate():
    data = request.json
    l = LotteryManager.add_participant(data["id"], data["choice"])
    if l:
        return (
            jsonify({"status": "success", "message": "Participant successfully added"}),
            201,
        )
    else:
        return (
            jsonify(
                {
                    "status": "failure",
                    "message": "A participant with the given id already exists",
                }
            ),
            200,
        )


def get_choice(participant_id: int):
    p = LotteryManager.get_participant(participant_id)
    if p is not None:
        return jsonify({"choice": p.choice}), 200
    else:
        return (
            jsonify(
                {
                    "status": "failed",
                    "message": "No user with the given participant id found",
                }
            ),
            404,
        )


def remove_participant(participant_id: int):
    LotteryManager.remove_participant(participant_id)
    return (
        jsonify({"status": "success", "message": "Participant successfully deleted"}),
        200,
    )
