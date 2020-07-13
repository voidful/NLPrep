import csv

from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "pttchat": [
            "https://raw.githubusercontent.com/zake7749/Gossiping-Chinese-Corpus/master/data/Gossiping-QA-Dataset-2_0.csv"]
    },
    'TASK': "gen",
    'FULLNAME': "PTT八卦版中文對話語料",
    'REF': {"Source": "https://github.com/zake7749/Gossiping-Chinese-Corpus"},
    'DESCRIPTION': """
    嗨，這裡是 PTT 中文語料集，我透過某些假設與方法 將每篇文章化簡為問答配對，其中問題來自文章的標題，而回覆是該篇文章的推文。
    """
}


def load(data):
    return data


def toMiddleFormat(paths):
    mf = MiddleFormat(DATASETINFO)
    for path in paths:
        with open(path, encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows, None)
            for row in rows:
                input = row[0]
                target = row[1]
                mf.add_data(input, target)
    return mf
