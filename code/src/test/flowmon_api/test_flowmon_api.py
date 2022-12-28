from src.flowmon_api import is_real_event


class TestFlowmonApi:
    def test_is_real_event(self):
        assert is_real_event(3054669)
        assert not is_real_event(-20)
        assert not is_real_event(100000000000000000)


