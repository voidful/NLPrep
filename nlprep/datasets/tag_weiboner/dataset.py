from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "weiboner-train": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.train",
        "weiboner-test": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.test",
        "weiboner-dev": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.dev",
    },
    'TASK': "tag",
    'FULLNAME': "Weibo NER dataset",
    'REF': {"Source": "https://github.com/hltcoe/golden-horse"},
    'DESCRIPTION': 'Entity Recognition (NER) for Chinese Social Media (Weibo). This dataset contains messages selected from Weibo and annotated according to the DEFT ERE annotation guidelines.'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8', errors='replace') as f:
        sent_input = []
        sent_target = []
        for i in list(f.readlines()):
            i = i.strip()
            if len(i) > 1:
                sent, tar = i.split('	')
                sent_input.append(sent)
                sent_target.append(tar)
            else:
                dataset.add_data(sent_input, sent_target)
                sent_input = []
                sent_target = []
    return dataset
