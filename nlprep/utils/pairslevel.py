import random
import sys
import inspect
from transformers import *
import nlp2

separate_token = "[SEP]"


def splitdata(path, pair, seed=612, train_ratio=0.7, test_ratio=0.2, valid_ratio=0.1):
    random.seed(seed)
    random.shuffle(pair)
    train_ratio = float(train_ratio)
    test_ratio = float(test_ratio)
    valid_ratio = float(valid_ratio)
    assert train_ratio > test_ratio >= valid_ratio and round(train_ratio + test_ratio + valid_ratio) == 1.0
    train_num = int(len(pair) * train_ratio)
    test_num = train_num + int(len(pair) * test_ratio)
    valid_num = test_num + int(len(pair) * valid_ratio)
    return [[path + "_train", pair[:train_num]],
            [path + "_test", pair[train_num:test_num]],
            [path + "_valid", pair[test_num:valid_num]]]


def setSepToken(path, pair, sep_token="[SEP]"):
    global separate_token
    separate_token = sep_token
    for ind, p in enumerate(pair):
        input_sent = p[0]
        pair[ind][0] = input_sent.replace("[SEP]", sep_token)
    return [[path, pair]]


def setMaxLen(path, pair, maxlen=512, tokenizer="word", with_target=[True, False], handle_over=['remove', 'slice']):
    global separate_token
    maxlen = int(maxlen)
    if tokenizer == 'word':
        sep_func = nlp2.split_sentence_to_array
    elif tokenizer == 'char':
        sep_func = list
    else:
        if 'voidful/albert' in tokenizer:
            tok = BertTokenizer.from_pretrained(tokenizer)
        else:
            tok = AutoTokenizer.from_pretrained(tokenizer)
        sep_func = tok.tokenize
    new_sep_token = " ".join(sep_func(separate_token)).strip()
    small_than_max_pairs = []
    for ind, p in enumerate(pair):
        tok_input = sep_func(p[0] + " " + p[1]) if with_target else sep_func(p[0])
        if len(tok_input) < maxlen:
            small_than_max_pairs.append(p)
        elif handle_over == 'slice':
            exceed = len(tok_input) - maxlen + 3  # +3 for more flexible space to further avoid exceed
            first_sep_index = tok_input.index(new_sep_token) if new_sep_token in tok_input else len(tok_input)
            limit_len = first_sep_index - exceed
            if limit_len > 0:
                tok_input = tok_input[:limit_len] + tok_input[first_sep_index:]
                if tokenizer == 'char':
                    small_than_max_pairs.append([("".join(tok_input)).replace(new_sep_token, separate_token), p[1]])
                else:
                    small_than_max_pairs.append([(" ".join(tok_input)).replace(new_sep_token, separate_token), p[1]])
    print("Num of data before handle max len :", len(pair))
    print("Num of data after handle max len :", len(small_than_max_pairs))
    return [[path, small_than_max_pairs]]


# control all same tag data ratio in dataset
def setAllSameTagRate(path, pair, seed=612, rate=0.27):
    random.seed(seed)
    allsame_pair = []
    notsame_pair = []
    for p in pair:
        if len(set(p[1])) < 2:
            allsame_pair.append(p)
        else:
            notsame_pair.append(p)

    asnum = min(int(len(notsame_pair) * rate), len(allsame_pair))
    print("all same pair:", len(allsame_pair), "have diff pair:", len(notsame_pair), "ratio:", rate, "take:", asnum)
    random.shuffle(allsame_pair)
    result = allsame_pair[:asnum] + notsame_pair
    random.shuffle(result)
    return [[path, result]]


# remove all same tag in tagging dataset
def rmAllSameTag(path, pair):
    result_pair = []
    for p in pair:
        if len(set(p[1])) > 1:
            result_pair.append(p)
    return [[path, result_pair]]


def reverse(path, pair):
    for p in pair:
        p.reverse()
    return [[path, pair]]


PairsUtils = dict(inspect.getmembers(sys.modules[__name__],
                                     predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__))
