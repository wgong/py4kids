"""
https://requests-mock.readthedocs.io/en/latest/pytest.html
"""

import pytest
import re
import requests
import requests_mock

def test_url_cm():
    # context mgr
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        requests.get('http://test.com').text
        assert 'resp' == requests.get('http://test.com').text

def test_url_get_text(requests_mock):
    requests_mock.get('http://test.com', text='resp')
    actual = requests.get('http://test.com').text
    print(f"\nactual={actual}")
    assert 'resp' == actual 

def test_url_get_json(requests_mock):
    requests_mock.get('http://test.com', json={"id": 10})
    actual = requests.get('http://test.com').json()
    print(f"\nactual={actual}")
    assert 10 == actual["id"]

def test_url_post_json(requests_mock):
    return_value = {"id": 10, "key": "val"}
    requests_mock.post('http://test.com', json=return_value, status_code=200)
    resp = requests.post('http://test.com')
    assert 200 == resp.status_code
    actual = resp.json()
    print(f"\nactual={actual}")
    assert return_value == actual

def test_url_match():
    # Request Matching
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.mount('mock://', adapter)
    adapter.register_uri('GET', 'mock://test.com/path', text='resp')
    actual = session.get('mock://test.com/path').text
    print(f"\nactual={actual}")
    assert 'resp' == actual

    # requests_mock.ANY acts as wildcard to match anything: method, URL
    adapter.register_uri(requests_mock.ANY, 'mock://test.com/8', text='resp')
    actual = session.get('mock://test.com/8').text
    assert 'resp' == actual
    actual = session.post('mock://test.com/8').text
    assert 'resp' == actual

    adapter.register_uri(requests_mock.ANY, requests_mock.ANY, text='resp')
    actual = session.get('mock://test1.com/8').text
    assert 'resp' == actual
    actual = session.post('mock://test2.com/8').text
    assert 'resp' == actual

    matcher = re.compile('tester.com/a')
    adapter.register_uri('GET', matcher, text='resp')
    actual = session.get('mock://tester.com/a/b').text
    assert 'resp' == actual

