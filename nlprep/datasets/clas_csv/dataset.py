import csv

from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'TASK': "clas"
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if len(row[0].strip()) > 2 and len(row[1].strip()) > 2:
                dataset.add_data(row[0], row[1])
    return dataset
