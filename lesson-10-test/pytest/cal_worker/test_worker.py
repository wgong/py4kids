from unittest.mock import patch, Mock

import worker
from worker import Worker

class DummyHelper:
    def get_path(self, *args, **kwargs):
        return "test_pytest.py"

@patch("worker.Helper")
def test_patching_class(mk_helper):
    mk_helper.return_value = mk_call = Mock()
    mk_call.get_path.return_value = "test_path.py"
    wk_1 = Worker()
    mk_helper.assert_called_once_with("os")
    assert wk_1.work() == "test_path.py"


@patch("worker.Helper")
def test_patching_class2(mk_helper):
    mk_helper.return_value = DummyHelper()
    wk_2 = worker.Worker()
    mk_helper.assert_called_once_with("os")
    assert wk_2.work() == "test_pytest.py"
