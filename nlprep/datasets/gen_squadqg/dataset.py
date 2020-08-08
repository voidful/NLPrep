import nlp
import nlp2
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


def toMiddleFormat(data, context_max_len=450, answer_max_len=50):
    dataset = MiddleFormat(DATASETINFO)
    for d in data:
        context = nlp2.split_sentence_to_array(d['context'])
        answer = nlp2.split_sentence_to_array(d['answers']['text'][0])
        input_data = " ".join(context[:context_max_len]) + " [SEP] " + " ".join(answer[:answer_max_len])
        target_data = d['question']
        dataset.add_data(input_data, target_data)

    return dataset
