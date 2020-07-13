from nlprep.middleformat import MiddleFormat
import nlp

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "mathqa-train": 'train',
        "mathqa-validation": 'validation',
        "mathqa-test": 'test'
    },
    'TASK': "clas",
    'FULLNAME': "Math QA",
    'REF': {"Source url": "https://math-qa.github.io/math-QA/data/MathQA.zip"},
    'DESCRIPTION': 'Our dataset is gathered by using a new representation language to annotate over the AQuA-RAT dataset. AQuA-RAT has provided the questions, options, rationale, and the correct options.'
}


def load(data):
    return nlp.load_dataset('math_qa')[data]


def toMiddleFormat(data):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        input = d['Problem'] + " [SEP] " + d['options']
        target = d['correct']
        dataset.add_data(input, target)
    return dataset
