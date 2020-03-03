import csv

from nlprep.middleformat import MiddleFormat
import nlp2

DATASET_FILE_MAP = {
    "dataset": [
        "https://raw.githubusercontent.com/voidful/Gossiping-Chinese-Positive-Corpus/master/Gossiping-QA-pos-Dataset-2_0.csv"]
}


def toMiddleFormat(paths):
    dataset = MiddleFormat()
    for path in paths:
        with open(path, encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                input = row[0]
                target = row[1]
                if float(row[2]) > 0.75:
                    dataset.add_data(input, target)
    return dataset
