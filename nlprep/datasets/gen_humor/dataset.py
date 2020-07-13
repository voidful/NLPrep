from nlprep.middleformat import MiddleFormat
import csv

try:
    from phraseg import *
except ImportError:
    print("phraseg not install, plz install it from https://github.com/voidful/Phraseg")
    raise

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "cccl2019-dev": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_development.csv",
        "cccl2019-train": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_train.csv",
        "cccl2019-test": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_test.csv",
    },
    'TASK': "gen",
    'FULLNAME': "CCL2019-Chinese-Humor-Computation Dataset",
    'REF': {"Source": "https://github.com/DUTIR-Emotion-Group/CCL2019-Chinese-Humor-Computation"},
    'DESCRIPTION': '任務二提取出來，透過phraseg獲取關鍵字，生成幽默句子。'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    phraseg = Phraseg(path)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        next(rows, None)
        for row in tqdm(rows):
            input = " ".join([k for k, v in phraseg.extract_sent(row[1], filter=True)])
            target = row[1]
            dataset.add_data(input, target)
    return dataset
