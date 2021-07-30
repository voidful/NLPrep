from nlprep.middleformat import MiddleFormat
import datasets

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "conllpp-train": 'train',
        "conllpp-validation": 'validation',
        "conllpp-test": 'test'
    },
    'TASK': "tag",
    'FULLNAME': "CoNLLpp is a corrected version of the CoNLL2003 NER dataset",
    'REF': {"Home page": "https://huggingface.co/datasets/conllpp"},
    'DESCRIPTION': 'CoNLLpp is a corrected version of the CoNLL2003 NER dataset where labels of 5.38% of the sentences in the test set have been manually corrected. The training set and development set from CoNLL2003 is included for completeness.'
}

ner_tag = {
    0: "O",
    1: "B-PER",
    2: "I-PER",
    3: "B-ORG",
    4: "I-ORG",
    5: "B-LOC",
    6: "I-LOC",
    7: "B-MISC",
    8: "I-MISC"
}


def load(data):
    return datasets.load_dataset('conllpp')[data]


def toMiddleFormat(data):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        input = d['tokens']
        target = [ner_tag[i] for i in d['ner_tags']]
        dataset.add_data(input, target)
    return dataset
