from unittest.mock import patch

import worker

@patch("worker.Helper")
def test_patching_class(MockHelper):
    MockHelper.return_value.get_path.return_value = "testing"
    wk1 = worker.Worker()
    MockHelper.assert_called_once_with("db")
    assert wk1.work() == "testing"
