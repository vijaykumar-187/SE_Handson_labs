import pytest
from password_policy import check_password, strength, suggest_fix

#Example test cases:
def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []

def test_valid_password_is_good():
    assert strength("Abcdef1!") == "good"

#Write the rest of the test cases so that the code is 90- 100% covered.
