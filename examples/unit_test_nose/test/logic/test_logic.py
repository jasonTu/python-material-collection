# coding: utf-8
__author__ = 'Administrator'

from nose.tools import assert_equal

from logic_operator.logic_operator import foo


def test_foo():
    result = foo()
    assert_equal(True, result)
