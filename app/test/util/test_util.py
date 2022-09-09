# -*- coding: UTF-8 -*-

from util.util import dotset, get_ipv4_by_hostname
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

def test_get_ipv4_by_hostname():
    print(get_ipv4_by_hostname('www.baidu.com'))
    print(get_ipv4_by_hostname('www.4399.com'))