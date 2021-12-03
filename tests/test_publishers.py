from mib.events.publishers import EventPublishers
import pytest

class TestEventPublisher:

    @pytest.mark.parametrize("payload, ret",[ 
        ({},None),
        ({"users":[{
            "id":1,
            "points":1}
            ]
        },0)
    ])
    def test_publish_winners(self, payload, ret):
        assert EventPublishers.publish_lottery_winners(payload) == ret