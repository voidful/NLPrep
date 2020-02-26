import csv

from nlprep.middleformat import MiddleFormat
import nlp2

DATASET_FILE_MAP = {
    "dataset": [
        "https://raw.githubusercontent.com/zake7749/Gossiping-Chinese-Corpus/master/data/Gossiping-QA-Dataset-2_0.csv"]
}


def toMiddleFormat(paths):
    dataset = MiddleFormat()
    for path in paths:
        with open(path, encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                input = nlp2.spilt_sentence_to_array(row[0], True)
                target = nlp2.spilt_sentence_to_array(row[1], True)
                if len(input) + len(target) < 256:
                    input = " ".join(input)
                    target = " ".join(target)
                    dataset.add_data(input, target)
    return dataset
