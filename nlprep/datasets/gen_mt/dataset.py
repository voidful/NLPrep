from nlprep.middleformat import MiddleFormat
import csv

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "engcmn": "https://raw.githubusercontent.com/voidful/transformer-nmt/master/data/cmn.txt",
        "engyue": "https://raw.githubusercontent.com/voidful/transformer-nmt/master/data/yue.txt"
    },
    'TASK': "gen",
    'FULLNAME': "Tab-delimited Bilingual Sentence Pairs",
    'REF': {"Source": "http://www.manythings.org/anki/"},
    'DESCRIPTION': 'English + TAB + The Other Language + TAB + Attribution'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')
        for row in rows:
            input = row[0]
            target = row[1]
            dataset.add_data(input, target)
    return dataset
