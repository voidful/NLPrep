import json
import re

import nlp2

from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "train": "https://raw.githubusercontent.com/DRCKnowledgeTeam/DRCD/master/DRCD_training.json",
    "test": "https://raw.githubusercontent.com/DRCKnowledgeTeam/DRCD/master/DRCD_test.json",
    "dev": "https://raw.githubusercontent.com/DRCKnowledgeTeam/DRCD/master/DRCD_dev.json",
}

#: A string of Chinese stops.
STOPS = (
    '\uFF01'  # Fullwidth exclamation mark
    '\uFF1F'  # Fullwidth question mark
    '\uFF61'  # Halfwidth ideographic full stop
    '\u3002'  # Ideographic full stop
)

SPLIT_PAT = '([{}]”?)'.format(STOPS)


def split_text(text, maxlen, split_pat=SPLIT_PAT, greedy=False):
    if len(text) <= maxlen:
        return [text], [0]
    segs = re.split(split_pat, text)
    sentences = []
    for i in range(0, len(segs) - 1, 2):
        sentences.append(segs[i] + segs[i + 1])
    if segs[-1]:
        sentences.append(segs[-1])
    n_sentences = len(sentences)
    sent_lens = [len(s) for s in sentences]
    alls = []
    for i in range(n_sentences):
        length = 0
        sub = []
        for j in range(i, n_sentences):
            if length + sent_lens[j] <= maxlen or not sub:
                sub.append(j)
                length += sent_lens[j]
            else:
                break
        alls.append(sub)
        if j == n_sentences - 1:
            if sub[-1] != j:
                alls.append(sub[1:] + [j])
            break

    if len(alls) == 1:
        return [text], [0]

    if greedy:
        sub_texts = [''.join([sentences[i] for i in sub]) for sub in alls]
        starts = [0] + [sum(sent_lens[:i]) for i in range(1, len(alls))]
        return sub_texts, starts
    else:
        DG = {}
        N = len(alls)
        for k in range(N):
            tmplist = list(range(k + 1, min(alls[k][-1] + 1, N)))
            if not tmplist:
                tmplist.append(k + 1)
            DG[k] = tmplist

        routes = {}
        routes[N] = (0, -1)
        for i in range(N - 1, -1, -1):
            templist = []
            for j in DG[i]:
                cross = set(alls[i]) & (set(alls[j]) if j < len(alls) else set())
                w_ij = sum([sent_lens[k] for k in cross]) ** 2
                w_j = routes[j][0]
                w_i_ = w_ij + w_j
                templist.append((w_i_, j))
            routes[i] = min(templist)

        sub_texts, starts = [''.join([sentences[i] for i in alls[0]])], [0]
        k = 0
        while True:
            k = routes[k][1]
            sub_texts.append(''.join([sentences[i] for i in alls[k]]))
            starts.append(sum(sent_lens[: alls[k][0]]))
            if k == N - 1:
                break

    return sub_texts, starts


def filter(s):
    s = nlp2.full2half(s)
    return s.replace(" ", "_").replace('\t', "_").replace('\n', "_").replace('\r', "_").replace('\v', "_").replace('\f',
                                                                                                                   "_")


def toMiddleFormat(path):
    dataset = MiddleFormat()

    max_len = 507
    with open(path, encoding="utf-8", errors='replace') as dataset_file:
        dataset_json = json.loads(dataset_file.read())
        dataset_json = dataset_json['data']

    for item in dataset_json:
        for paragraph in item['paragraphs']:
            for qas in paragraph['qas']:
                qas['question'] = filter(qas['question'])
                question = list(qas['question'])
                question = ['[Question]'] + question
                for answers in qas['answers'][:1]:
                    paragraph['context'] = filter(paragraph['context'])
                    context = paragraph['context']
                    ans = filter(str(answers['text']))
                    ans_length = len(ans)
                    start = answers['answer_start']
                    end = start + ans_length
                    tag = ["O"] * len(context)
                    tag[start:end] = ["A"] * ans_length
                    context, tstart = split_text(context, max_len)
                    for i, c in enumerate(context):
                        c = list(c)
                        t = tag[tstart[i]:tstart[i] + len(c)]
                        c.extend(question)
                        t.extend(["O"] * len(question))
                        if "A" in t:
                            ind = t.index("A")
                            if "".join(c[ind:ind + ans_length]) != ans or len(c) != len(t):
                                pass
                        if len(c) < max_len:
                            dataset.add_data(c, t)

    return dataset
