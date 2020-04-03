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


# control all same tag data ratio in dataset
def tagsamerate(path, pair, rate=0.27, seed=422):
    random.seed(seed)
    allsame_pair = []
    notsame_pair = []
    for p in pair:
        if len(set(p[1])) < 2:
            allsame_pair.append(p)
        else:
            notsame_pair.append(p)

    asnum = min(int(len(notsame_pair) * rate), len(allsame_pair))
    print("allsame_pair:", len(allsame_pair), "notsame_pair:", len(notsame_pair), "ratio:", rate, "take:", asnum)
    random.shuffle(allsame_pair)
    result = allsame_pair[:asnum] + notsame_pair
    random.shuffle(result)
    return [path, result]


# remove all same tag in tagging dataset
def tagrmallsame(path, pair):
    result_pair = []
    for p in pair:
        if len(set(p[1])) > 1:
            result_pair.append(p)
    return [path, result_pair]


def reverse(path, pair):
    for p in pair:
        p.reverse()
    return [path, pair]


PairsUtils = dict(inspect.getmembers(sys.modules[__name__],
                                     predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__))
