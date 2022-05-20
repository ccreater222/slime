# -*- coding: UTF-8 -*-
from util.util import dotset
def test_dotset():
    test = {
        'a' : 'b',
        'b' : [1],
        'c' : {
            'e': 'f'
        }
    }
    result = dotset(test)
    assert ['a', 'b'] in result
    assert ['b', [1]] in result
    assert ['c.e', 'f'] in result