from nlprep.middleformat import MiddleFormat
import nlp2
import csv

try:
    from phraseg import *
except ImportError:
    print("phraseg not install, plz install it from https://github.com/voidful/Phraseg")
    raise

DATASET_FILE_MAP = {
    "humor-dev": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_development.csv",
    "humor-train": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_train.csv",
    "humor-test": "https://raw.githubusercontent.com/voidful/CCL2019-Chinese-Humor-Computation/master/task2/task2_test.csv",
}


def toMiddleFormat(path):
    dataset = MiddleFormat()
    phraseg = Phraseg(path)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        next(rows, None)
        for row in rows:
            input = [k for k, v in phraseg.extract_sent(row[1], filter=True)]
            target = nlp2.spilt_sentence_to_array(row[1], True)
            if len(input) + len(target) <= 512:
                input = " ".join(input)
                target = " ".join(target)
                dataset.add_data(input, target)
    return dataset
