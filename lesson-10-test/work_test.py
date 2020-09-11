
from unittest.mock import patch

from work import work_on

@patch("work.os.getcwd", return_value="testing")
def test_getcwd(*args):
    assert work_on() == "testing"
