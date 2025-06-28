import pytest

from src.atc.core.speech import Speech


@pytest.fixture
def speech():
    return Speech()


def test_explain_zh_digits(speech: Speech):
    assert speech.explain_zh("123") == "幺两三"
    assert speech.explain_zh("908") == "九洞八"
    assert speech.explain_zh("123.7") == "幺两三点拐"
    assert speech.explain_zh("7700") == "拐拐洞洞"


def test_explain_zh_mixed_alphanum(speech: Speech):
    assert speech.explain_zh("A1B2") == "alpha 幺 bravo 两"
    assert speech.explain_zh("Z9") == "zulu 九"


def test_explain_zh_empty(speech: Speech):
    assert speech.explain_zh("") == ""


def test_explain_zh_spaces(speech: Speech):
    assert speech.explain_zh("1 2") == "幺 两"
    assert speech.explain_zh(" 3 ") == "三"


def test_explain_zh_letters_with_spaces(speech: Speech):
    assert speech.explain_zh("A B C") == "alpha bravo charlie"


def test_explain_en_digits(speech: Speech):
    assert speech.explain_en("123") == "one two tree"
    assert speech.explain_en("908") == "niner zero eight"
    assert speech.explain_en("121.5") == "one two one decimal fife"
    assert speech.explain_en("7700") == "seven seven zero zero"


def test_explain_en_mixed_alphanum(speech: Speech):
    assert speech.explain_en("MH370") == "mike hotel tree seven zero"
    assert speech.explain_en("AF447") == "alpha foxtrot fower fower seven"
    assert speech.explain_en("P23S3") == "papa two tree sierra tree"


def test_explain_en_empty(speech: Speech):
    assert speech.explain_en("") == ""


def test_explain_en_spaces(speech: Speech):
    assert speech.explain_en("1 2") == "one two"
    assert speech.explain_en(" 3 ") == "tree"
