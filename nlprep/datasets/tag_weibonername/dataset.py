from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "weibonername-train": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.train",
        "weibonername-test": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.test",
        "weibonername-dev": "https://raw.githubusercontent.com/hltcoe/golden-horse/master/data/weiboNER.conll.dev",
    },
    'TASK': "tag",
    'FULLNAME': "Weibo NER dataset with only name",
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
                if "PER.NAM" not in tar:
                    tar = 'O'
                else:
                    tar = tar.replace(".NAM", "")
                sent_target.append(tar)
            else:
                dataset.add_data(sent_input, sent_target)
                sent_input = []
                sent_target = []
    return dataset
