
from password_policy import check_password, strength, suggest_fix


# ==========================================
# BRANCH COVERAGE TESTS
# ==========================================

# check_password(): Length decision branches

def test_password_length_below_8():
    assert "too short" in check_password("Ab1!")


def test_password_length_exactly_8():
    assert "too short" not in check_password("Abcdef1!")


def test_password_length_above_64():
    password = "A" * 65 + "a1!"
    assert "too long" in check_password(password)


# Common password decision branches

def test_common_password_true():
    assert "common" in check_password("password")


def test_common_password_false():
    assert "common" not in check_password("Abcdef1!")


# Character classification branches

def test_uppercase_branch():
    assert "no uppercase" not in check_password("Aabcdef1!")


def test_lowercase_branch():
    assert "no lowercase" in check_password("ABCDEFG1!")


def test_digit_branch():
    assert "no digit" in check_password("Abcdefgh!")


def test_special_character_branch():
    assert "no special" in check_password("Abcdefg1")


# strength(): Decision branches

def test_strength_no_issues():
    assert strength("Abcdef1!") == "good"


def test_strength_14_or_more_characters():
    assert strength("Abcdefghijk1!X") == "strong"


def test_strength_one_or_two_issues():
    assert strength("abcdefg1") == "weak"


def test_strength_more_than_two_issues():
    assert strength("abc") == "very weak"


# suggest_fix(): Decision branches

def test_fix_empty_issues():
    assert suggest_fix([]) == "none needed"


def test_fix_too_short_branch():
    assert suggest_fix(["too short"]) == "add more characters"


def test_fix_common_branch():
    assert suggest_fix(["common"]) == "avoid common passwords"


def test_fix_no_prefix_branch():
    assert suggest_fix(["no digit"]) == "add digit"


def test_fix_other_issue_branch():
    assert suggest_fix(["too long"]) == "shorten it"
