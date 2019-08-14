import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, Verbosity


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
def test_sum(num1, num2):
    assert sum(num1, num2) == num1 + num2
