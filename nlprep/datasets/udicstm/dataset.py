from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "dataset": ["https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twpos.txt",
                "https://raw.githubusercontent.com/UDICatNCHU/UdicOpenData/master/udicOpenData/Snownlp訓練資料/twneg.txt"]
}


def toMiddleFormat(paths):
    dataset = MiddleFormat()
    for path in paths:
        with open(path, encoding='utf8') as f:
            if "失望" in f.readline():
                sentiment = "negative"
            else:
                sentiment = "positive"
            for i in list(f.readlines()):
                dataset.add_data(i.strip(), sentiment)
    return dataset
