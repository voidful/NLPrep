from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "udicstm": [
            "https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twpos.txt",
            "https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twneg.txt"]
    },
    'TASK': "clas",
    'FULLNAME': "UDIC Sentiment Analysis Dataset",
    'REF': {"Source": "https://github.com/UDICatNCHU/UdicOpenData"},
    'DESCRIPTION': '正面情緒：約有309163筆，44M / 負面情緒：約有320456筆，15M'
}


def load(data):
    return data


def toMiddleFormat(paths):
    dataset = MiddleFormat(DATASETINFO)
    for path in paths:
        with open(path, encoding='utf8') as f:
            if "失望" in f.readline():
                sentiment = "negative"
            else:
                sentiment = "positive"
            for i in list(f.readlines()):
                dataset.add_data(i.strip(), sentiment)
    return dataset
