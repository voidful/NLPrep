from nlprep.middleformat import MiddleFormat
import nlp2
import csv

try:
    from phraseg import *
except ImportError:
    print("phraseg not install, plz install it from https://github.com/voidful/Phraseg")
    raise

DATASET_FILE_MAP = {
    "poetry": "https://raw.githubusercontent.com/voidful/poetry/master/poetry.csv"
}
TYPE = "gen"

def toMiddleFormat(path):
    dataset = MiddleFormat(TYPE)
    phraseg = Phraseg(path)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if len(row) > 0:
                input = [k for k, v in phraseg.extract_sent(row[0], filter=True)]
                target = row[0].split()
                if len(input) + len(target) <= 512:
                    input = " ".join(input)
                    target = " ".join(list(row[0].replace(" ", "")))
                    dataset.add_data(input, target)
    return dataset
