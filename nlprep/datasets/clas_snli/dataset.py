from nlprep.middleformat import MiddleFormat
import nlp

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "snli-train": 'train',
        "snli-validation": 'validation',
        "snli-test": 'test'
    },
    'TASK': "clas",
    'FULLNAME': "Stanford Natural Language Inference (SNLI) Corpus",
    'REF': {"Home page": "https://nlp.stanford.edu/projects/snli/"},
    'DESCRIPTION': 'The SNLI corpus (version 1.0) is a collection of 570k human-written English sentence pairs manually labeled for balanced classification with the labels entailment, contradiction, and neutral, supporting the task of natural language inference (NLI), also known as recognizing textual entailment (RTE).'
}


def load(data):
    return nlp.load_dataset('snli')[data]


def toMiddleFormat(data):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        input = d['premise'] + " [SEP] " + d['hypothesis']
        target = d['label']
        dataset.add_data(input, target)
    return dataset
