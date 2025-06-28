import pytest

from src.atc.core.speech import Speech


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("123", "幺两三"),
        ("908", "九洞八"),
        ("123.7", "幺两三点拐"),
        ("7700", "拐拐洞洞"),
        ("A1B2", "alpha 幺 bravo 两"),
        ("Z9", "zulu 九"),
        ("1 2", "幺 两"),
        (" 3 ", "三"),
        ("A B C", "alpha bravo charlie"),
        ("", ""),
    ],
)
def test_explain_zh(input_text: str, expected: str):
    assert Speech.explain_zh(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("123", "one two tree"),
        ("908", "niner zero eight"),
        ("121.5", "one two one decimal fife"),
        ("7700", "seven seven zero zero"),
        ("MH370", "mike hotel tree seven zero"),
        ("AF447", "alpha foxtrot fower fower seven"),
        ("P23S3", "papa two tree sierra tree"),
        ("1 2", "one two"),
        (" 3 ", "tree"),
        ("A B C", "alpha bravo charlie"),
        ("", ""),
    ],
)
def test_explain_en(input_text: str, expected: str):
    assert Speech.explain_en(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("18L", "幺八左"),
        ("36R", "三六右"),
        ("09", "洞九"),
        ("20C", "两洞中"),
    ],
)
def test_explain_rwy_zh(input_text: str, expected: str):
    assert Speech.explain_rwy_zh(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("18L", "one eight left"),
        ("36R", "tree six right"),
        ("09", "zero niner"),
        ("12C", "one two center"),
    ],
)
def test_explain_rwy_en(input_text: str, expected: str):
    assert Speech.explain_rwy_en(input_text) == expected
