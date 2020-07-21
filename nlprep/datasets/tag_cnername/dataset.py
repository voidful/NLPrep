from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "cnername-train": "https://raw.githubusercontent.com/zjy-ucas/ChineseNER/master/data/example.train",
        "cnername-test": "https://raw.githubusercontent.com/zjy-ucas/ChineseNER/master/data/example.test",
        "cnername-dev": "https://raw.githubusercontent.com/zjy-ucas/ChineseNER/master/data/example.dev",
    },
    'TASK': "tag",
    'FULLNAME': "ChineseNER with only name",
    'REF': {"Source": "https://github.com/zjy-ucas/ChineseNER"},
    'DESCRIPTION': 'From https://github.com/zjy-ucas/ChineseNER/tree/master/data, source unknown.'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8') as f:
        sent_input = []
        sent_target = []
        for i in list(f.readlines()):
            i = i.strip()
            if len(i) > 1:
                sent, tar = i.split(' ')
                sent_input.append(sent)
                if "PER" not in tar:
                    tar = 'O'
                sent_target.append(tar)
            else:
                dataset.add_data(sent_input, sent_target)
                sent_input = []
                sent_target = []
    return dataset
