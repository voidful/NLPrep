import sys
import inspect

from opencc import OpenCC

cc_t2s = OpenCC('t2s')
cc_s2t = OpenCC('s2t')


def s2t(convt):
    """simplify chines to traditional chines"""
    return cc_s2t.convert(convt)


def t2s(convt):
    """traditional chines to simplify chines"""
    return cc_t2s.convert(convt)


SentUtils = dict(inspect.getmembers(sys.modules[__name__],
                                    predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__))
