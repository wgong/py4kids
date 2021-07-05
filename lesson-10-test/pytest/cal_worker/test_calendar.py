import pytest
from requests.exceptions import Timeout
from unittest.mock import Mock

# Mock requests to control its behavior
requests = Mock()

def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None

def test_get_holidays_timeout():
    # Test a connection timeout
    requests.get.side_effect = Timeout
    with pytest.raises(Timeout):
        get_holidays()
