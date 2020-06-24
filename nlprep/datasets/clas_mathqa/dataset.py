from nlprep.middleformat import MiddleFormat
import nlp

dataset = nlp.load_dataset('math_qa')

DATASET_FILE_MAP = {
    "train": dataset['train'],
    "validation": dataset['validation'],
    "test": dataset['test']
}
TYPE = "clas"


def toMiddleFormat(data):
    dataset = MiddleFormat(TYPE)
    for d in data:
        input = d['Problem'] + " [SEP] " + d['options']
        target = d['correct']
        dataset.add_data(input, target)
    return dataset
