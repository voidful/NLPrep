from nlprep.middleformat import MiddleFormat
import nlp

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "cosmosqa-train": 'train',
        "cosmosqa-validation": 'validation',
        "cosmosqa-test": 'test'
    },
    'TASK': "clas",
    'FULLNAME': "Cosmos QA",
    'REF': {"HomePage": "https://wilburone.github.io/cosmos/",
            "Dataset": " https://github.com/huggingface/nlp/blob/master/datasets/cosmos_qa/cosmos_qa.py"},
    'DESCRIPTION': "Cosmos QA is a large-scale dataset of 35.6K problems that require commonsense-based reading comprehension, formulated as multiple-choice questions. It focuses on reading between the lines over a diverse collection of people's everyday narratives, asking questions concerning on the likely causes or effects of events that require reasoning beyond the exact text spans in the context"
}


def load(data):
    return nlp.load_dataset('cosmos_qa')[data]


def toMiddleFormat(data):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        input = d['context'] + " [SEP] " + d['question'] + " [SEP] " + d['answer0'] + " [SEP] " + d[
            'answer1'] + " [SEP] " + d['answer2'] + " [SEP] " + d['answer3']
        target = d['label']
        dataset.add_data(input, target)
    return dataset
