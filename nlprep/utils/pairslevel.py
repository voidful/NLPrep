import random
import sys
import inspect


def splittrain(path, pair, seed=422, ratio=0.7):
    random.seed(seed)
    random.shuffle(pair)
    train_num = int(len(pair) * ratio)
    path += "_train"
    return [path, pair[:train_num]]


def splittest(path, pair, seed=422, train_ratio=0.7, test_ratio=0.2):
    random.seed(seed)
    random.shuffle(pair)
    train_num = int(len(pair) * train_ratio)
    test_num = train_num + int(len(pair) * test_ratio)
    path += "_test"
    return [path, pair[train_num:test_num]]


def splitvalid(path, pair, seed=422, train_ratio=0.7, test_ratio=0.2, valid_ratio=0.1):
    random.seed(seed)
    random.shuffle(pair)
    train_num = int(len(pair) * train_ratio)
    test_num = train_num + int(len(pair) * test_ratio)
    valid_num = test_num + int(len(pair) * valid_ratio)
    path += "_valid"
    return [path, pair[test_num:valid_num]]


PairsUtils = dict(inspect.getmembers(sys.modules[__name__],
                                     predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__))
