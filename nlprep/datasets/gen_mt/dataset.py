from nlprep.middleformat import MiddleFormat
import nlp2
import csv

DATASET_FILE_MAP = {
    "engcmn": "https://raw.githubusercontent.com/voidful/transformer-nmt/master/data/cmn.txt",
    "engyue": "https://raw.githubusercontent.com/voidful/transformer-nmt/master/data/yue.txt"
}
TYPE = "gen"

def toMiddleFormat(path):
    dataset = MiddleFormat(TYPE)
    with open(path, encoding='utf8') as csvfile:
        rows = csv.reader(csvfile, delimiter='\t')
        for row in rows:
            input = nlp2.split_sentence_to_array(row[0], True)
            target = nlp2.split_sentence_to_array(row[1], True)
            if len(input) + len(target) <= 512:
                input = " ".join(input)
                target = " ".join(target)
                dataset.add_data(input, target)
    return dataset
