from nlprep.middleformat import MiddleFormat
import nlp

dataset = nlp.load_dataset('snli')

DATASET_FILE_MAP = {
    "train": dataset['train'],
    "validation": dataset['validation'],
    "test": dataset['test']
}
TYPE = "clas"


def toMiddleFormat(data):
    dataset = MiddleFormat(TYPE)
    for d in data:
        input = d['premise'] + " [SEP] " + d['hypothesis']
        target = d['label']
        dataset.add_data(input, target)
    return dataset
