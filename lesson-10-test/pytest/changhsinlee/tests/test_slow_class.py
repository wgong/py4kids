from src.main import slow_dataset
from unittest.mock import patch

def mock_load(*args, **kwargs):
    return 'xyz'


def test_mocking_class_method(mocker):
    expected = 'xyz'

    # def mock_load(self):
    #     return 'xyz'

    mocker.patch(
        'src.main.Dataset.load_data',
        mock_load
    )
    actual = slow_dataset()
    assert expected == actual

@patch('src.main.Dataset.load_data',mock_load)
def test_mocking_class_method2(mocker):
    expected = 'xyz'
    actual = slow_dataset()
    assert expected == actual
