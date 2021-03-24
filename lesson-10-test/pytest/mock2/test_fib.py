from fn import fib
import pytest


def test_fib_1():
    assert fib(0) == 0
    assert fib(1) == 1

@pytest.mark.skip
def test_fib_2():
    assert fib(10) == 55