#!/usr/bin/env python3

import fn
import pytest

@pytest.fixture
def data():
    return [3, 2, 1, 5, -3, 2, 0, -2, 11, 9]

def test_sel_sort(data):
    sorted_vals = fn.sel_sort(data)
    assert sorted_vals == sorted(data)

def test_min():
    values = (2, 3, 1, 4, 6)
    val = fn.min(values)
    assert val == 1

def test_max():
    values = (2, 3, 1, 4, 6)

    val = fn.max(values)
    assert val == 6

@pytest.mark.parametrize(
    "word, expected", [
    ('kayak', True), 
    ('civic', True), 
    ('forest', False)
])
def test_palindrome(word, expected):

    val = fn.is_palindrome(word)
    assert val == expected