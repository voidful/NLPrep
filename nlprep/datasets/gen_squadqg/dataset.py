import json

import nlp
from tqdm import tqdm
from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "squad-qg-train": "train",
        "squad-qg-dev": "validation"
    },
    'TASK': "gen",
    'FULLNAME': "The Stanford Question Answering Dataset 2.0",
    'REF': {"Source": "https://rajpurkar.github.io/SQuAD-explorer/"},
    'DESCRIPTION': 'Question Generate For SQuAD 2.0'
}


def load(data):
    return nlp.load_dataset('squad')[data]


def toMiddleFormat(data):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        input_data = d['context'] + " [SEP] " + d['answers']['text'][0]
        target_data = d['question']
        dataset.add_data(input_data, target_data)

    return dataset
