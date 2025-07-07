"""
语音管理。
"""

from typing import Union


_DIGIT_ZH = {
    "0": "洞",
    "1": "幺",
    "2": "两",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "拐",
    "8": "八",
    "9": "九",
    ".": "点",
}
_DIGIT_EN = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "tree",
    "4": "fower",
    "5": "fife",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "niner",
    ".": "decimal",
}
_ALPHABET = {
    "A": "alpha",
    "B": "bravo",
    "C": "charlie",
    "D": "delta",
    "E": "echo",
    "F": "foxtrot",
    "G": "golf",
    "H": "hotel",
    "I": "india",
    "J": "juliet",
    "K": "kilo",
    "L": "lima",
    "M": "mike",
    "N": "november",
    "O": "oscar",
    "P": "papa",
    "Q": "quebec",
    "R": "romeo",
    "S": "sierra",
    "T": "tango",
    "U": "uniform",
    "V": "victor",
    "W": "whiskey",
    "X": "x-ray",
    "Y": "yankee",
    "Z": "zulu",
}


class Speech:
    """
    语音管理。
    """

    @staticmethod
    def explain_zh(text: Union[str, object]) -> str:
        """
        将文本转换为中文语音格式。
        """
        if isinstance(text, object):
            text = str(text)
        text = "".join(_DIGIT_ZH.get(c, c) for c in text)
        return Speech._explain_alphabet(text)

    @staticmethod
    def explain_en(text: Union[str, object]) -> str:
        """
        将文本转换为英文语音格式。
        """
        if isinstance(text, object):
            text = str(text)
        text = " ".join(_DIGIT_EN.get(c, c) for c in text)
        return Speech._explain_alphabet(text)

    @staticmethod
    def _explain_alphabet(text: str) -> str:
        for char, repl in _ALPHABET.items():
            text = text.replace(char, f" {repl} ")
        return text.replace("  ", " ").replace("  ", " ").replace("  ", " ").strip()

    @staticmethod
    def explain_rwy_zh(rwy: str) -> str:
        """
        将跑道号转换为中文语音格式。
        """
        rwy = rwy.replace("L", "左").replace("R", "右").replace("C", "中")
        return Speech.explain_zh(rwy)

    @staticmethod
    def explain_rwy_en(rwy: str) -> str:
        """
        将跑道号转换为英文语音格式。
        """
        suffix = None
        match rwy[-1]:
            case "L":
                suffix = "left"
            case "R":
                suffix = "right"
            case "C":
                suffix = "center"

        return Speech.explain_en(rwy[:2]) + (" " + suffix if suffix else "")
