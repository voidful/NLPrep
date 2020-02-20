from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "dataset": ["https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twpos.txt",
                "https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twneg.txt"]
}


def toMiddleFormat(paths):
    dataset = MiddleFormat()
    for path in paths:
        with open(path, encoding='utf8') as f:
            if 'pos' in path:
                sentiment = "positive"
            else:
                sentiment = "negative"
            for i in list(f.readlines()):
                dataset.add_data(i.strip(), sentiment)
    return dataset
