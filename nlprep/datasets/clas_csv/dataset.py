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
            dataset.add_data(row[0], row[1])
    return dataset
