import pytest

from mib.events.publishers import EventPublishers


class TestEventPublisher:
    @pytest.mark.parametrize(
        "payload, ret", [({}, None), ({"users": [{"id": 1, "points": 1}]}, 0)]
    )
    def test_publish_winners(self, payload, ret):
        assert EventPublishers.publish_lottery_winners(payload) == ret

    @pytest.mark.parametrize("payload, ret", [({}, None), ({"notifications": [{}]}, 0)])
    def test_publish_notify(self, payload, ret):
        assert EventPublishers.publish_notify_winners(payload) == ret
