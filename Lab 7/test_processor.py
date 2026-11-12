from hypothesis import given, strategies as st

from processor import (
    first_character_type,
    split_credentials,
    digit_ratio,
)


@given(st.text() | st.none())
def test_first_character_type_no_crash(value):
    first_character_type(value)


@given(st.text() | st.none())
def test_split_credentials_no_crash(value):
    split_credentials(value)


@given(st.text() | st.none())
def test_digit_ratio_no_crash(value):
    digit_ratio(value)
