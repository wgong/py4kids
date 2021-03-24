#!/usr/bin/env python3

import utils.fn
import pytest

@pytest.fixture
def data():
    return [3, 2, 1, 5, -3, 2, 0, -2, 11, 9]

def test_sel_sort(data):
    sorted_vals = utils.fn.sel_sort(data)
    assert sorted_vals == sorted(data)

def test_min():
    values = (2, 3, 1, 4, 6)
    val = utils.fn.min(values)
    assert val == 1

def test_max():
    values = (2, 3, 1, 4, 6)

    val = utils.fn.max(values)
    assert val == 6

@pytest.mark.parametrize(
    "word, expected", [
    ('kayak', True), 
    ('civic', True), 
    ('forest', False)
])
def test_palindrome(word, expected):

    val = utils.fn.is_palindrome(word)
    assert val == expected