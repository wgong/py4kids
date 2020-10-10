from hypothesis import given, example
from hypothesis.strategies import text

from enc_dec import encode,decode

@given(text())
@example(s="")
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s