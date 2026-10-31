
from password_policy import check_password, strength, suggest_fix


# ==========================================
# CODE COVERAGE TESTS
# ==========================================

# 1. check_password() tests

def test_valid_password():
    assert check_password("Abcdef1!") == []


def test_password_too_short():
    assert "too short" in check_password("Ab1!")


def test_password_too_long():
    password = "Aa1!" * 17
    assert "too long" in check_password(password)


def test_common_password():
    assert "common" in check_password("password")


def test_password_without_uppercase():
    assert "no uppercase" in check_password("abcdefg1!")


def test_password_without_lowercase():
    assert "no lowercase" in check_password("ABCDEFG1!")


def test_password_without_digit():
    assert "no digit" in check_password("Abcdefgh!")


def test_password_without_special_character():
    assert "no special" in check_password("Abcdefg1")


def test_password_with_all_character_types():
    assert check_password("StrongPass123!") == []


# 2. strength() tests

def test_good_password_strength():
    assert strength("Abcdef1!") == "good"


def test_strong_password_strength():
    assert strength("Abcdefghijk1!X") == "strong"


def test_weak_password_strength():
    assert strength("abcdefg1") == "weak"


def test_very_weak_password_strength():
    assert strength("abc") == "very weak"


# 3. suggest_fix() tests

def test_suggest_fix_no_issues():
    assert suggest_fix([]) == "none needed"


def test_suggest_fix_too_short():
    assert suggest_fix(["too short", "no uppercase"]) == "add more characters"


def test_suggest_fix_common_password():
    assert suggest_fix(["common", "no digit"]) == "avoid common passwords"


def test_suggest_fix_missing_character():
    assert suggest_fix(["no uppercase"]) == "add uppercase"


def test_suggest_fix_too_long():
    assert suggest_fix(["too long"]) == "shorten it"
