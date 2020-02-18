import sys
import inspect

from opencc import OpenCC
cc_t2s = OpenCC('t2s')
cc_s2t = OpenCC('s2t')


def s2t(convt):
    return cc_s2t.convert(convt)


def t2s(convt):
    return cc_t2s.convert(convt)


utilsList = dict(inspect.getmembers(sys.modules[__name__],
                               predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__))
