import pytest

from sympy import Expr, simplify

from atc.core.scene.aircraft.vector_sym import VectorSym2


@pytest.mark.parametrize(
    "x,y",
    [(simplify("x**2+2*x"), simplify("3*x-4"))],
)
def test_vectorsym2_init(x: Expr, y: Expr):
    v = VectorSym2(x, y)
    assert v.x == x
    assert v.y == y


@pytest.mark.parametrize(
    "x,y",
    [(simplify("x**2+2*x"), simplify("3*x-4"))],
)
def test_vectorsym2_copy(x: Expr, y: Expr):
    v1 = VectorSym2(x, y)
    v2 = v1.copy()
    assert v1.x == v2.x == x
    assert v1.y == v2.y == y


@pytest.mark.parametrize(
    "v1,v2,expected",
    [
        (
            VectorSym2(simplify("x**2+2*x"), simplify("3*x-4")),
            VectorSym2(simplify("x-4"), simplify("sqrt(x)+2*x**2")),
            VectorSym2(simplify("x**2+3*x-4"), simplify("2*x**2+3*x-4+sqrt(x)")),
        ),
        (
            VectorSym2(simplify("(x+1)**2"), simplify("3*x-4")),
            VectorSym2(simplify("x-4"), simplify("sqrt(x)+2*x**2")),
            VectorSym2(simplify("x**2+3*x-3"), simplify("2*x**2+3*x-4+sqrt(x)")),
        ),
    ],
)
def test_vectorsym2_add(v1: VectorSym2, v2: VectorSym2, expected: VectorSym2):
    assert v1 + v2 == expected


@pytest.mark.parametrize(
    "v1,v2,expected",
    [
        (
            VectorSym2(simplify("x**2+2*x"), simplify("3*x-4")),
            VectorSym2(simplify("-x+4"), simplify("-sqrt(x)-2*x**2")),
            VectorSym2(simplify("x**2+3*x-4"), simplify("2*x**2+3*x-4+sqrt(x)")),
        ),
        (
            VectorSym2(simplify("(x+1)**2"), simplify("3*x-4")),
            VectorSym2(simplify("x-4"), simplify("sqrt(x)+2*x**2")),
            VectorSym2(simplify("x**2+x+5"), simplify("-2*x**2+3*x-4-sqrt(x)")),
        ),
    ],
)
def test_vectorsym2_sub(v1: VectorSym2, v2: VectorSym2, expected: VectorSym2):
    assert v1 - v2 == expected


@pytest.mark.parametrize(
    "v1,v2",
    [
        (
            VectorSym2(simplify("x**2+2*x"), simplify("3*x-4")),
            VectorSym2(simplify("(x+1)**2-1"), simplify("-sqrt(x)+3*x+x**(1/2)-4")),
        ),
        (
            VectorSym2(simplify("x**2"), simplify("y*6+8")),
            VectorSym2(simplify("(x+1)**2-2*x-1"), simplify("-y**2+(y+3)**2+(-1)")),
        ),
    ],
)
def test_vectorsym2_eq(v1: VectorSym2, v2: VectorSym2):
    assert v1 == v2
