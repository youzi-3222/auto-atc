"""
可以用未知数表示的二维向量。
"""

from pygame import Vector2
from sympy import Expr


class VectorSym2:
    """
    可以用未知数表示的二维向量。
    """

    x: Expr
    y: Expr

    def __init__(self, x: Expr, y: Expr) -> None:
        self.x = x
        self.y = y

    def copy(self):
        """
        复制该对象。
        """
        return VectorSym2(self.x, self.y)

    def __add__(self, other: object):
        if not isinstance(other, (VectorSym2, Vector2)):
            raise TypeError(f"VectorSym2 不能与 {type(other)} 相加")
        return VectorSym2(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return VectorSym2(-self.x, -self.y)

    def __sub__(self, other: object):
        if not isinstance(other, (VectorSym2, Vector2)):
            raise TypeError(f"VectorSym2 不能与 {type(other)} 相加")
        return self + (-other)

    def __eq__(self, other: object):
        if not isinstance(other, (VectorSym2, Vector2)):
            return False
        if isinstance(other, VectorSym2):
            return (
                self.x.expand() == other.x.expand()
                and self.y.expand() == other.y.expand()
            )
        return self.x.expand() == other.x and self.y.expand() == other.y
