import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, Verbosity, example


def sum(num1, num2):
    return num1 + num2


"""
@pytest.mark.parametrize(
    'num1, num2, expected', [(3, 4, 7), (3, 0, 3), (-3, 4, 1), (3, 5, 8)]
)
def test_sum(num1, num2, expected):
    assert sum(num1, num2) == expected
"""

@settings(verbosity=Verbosity.verbose)
@given(st.integers(), st.integers())
@example(1, 2)
def test_sum(num1, num2):
    assert sum(num1, num2) == num1 + num2
    assert sum(num1, 0) == num1
    assert sum(num1, num2) == sum(num2, num1)
    # assert num1 <= 30
