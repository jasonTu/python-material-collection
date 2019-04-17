# coding: utf-8
__author__ = 'Administrator'


from nose.tools import with_setup
from nose.tools import assert_equal

import mymath.math as mmath


def test_math_add():
    result = mmath.add(1, 2)
    assert_equal(3, result)
