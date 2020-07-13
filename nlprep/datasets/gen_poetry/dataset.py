from nlprep.middleformat import MiddleFormat
import csv

try:
    from phraseg import *
except ImportError:
    print("phraseg not install, plz install it from https://github.com/voidful/Phraseg")
    raise

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "poetry": "https://raw.githubusercontent.com/voidful/poetry/master/poetry.csv"
    },
    'TASK': "gen",
    'FULLNAME': "關鍵字生成全唐詩",
    'REF': {"Source": "https://github.com/chinese-poetry/chinese-poetry"},
    'DESCRIPTION': 'Phraseg統計關鍵字 然後根據統計的關鍵字生成唐詩'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    phraseg = Phraseg(path)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if len(row) > 0:
                input = " ".join([k for k, v in phraseg.extract_sent(row[0], filter=True)])
                target = row[0]
                dataset.add_data(input, target)

    return dataset
