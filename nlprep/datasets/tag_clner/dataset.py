from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "clner-train": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/train.txt",
        "clner-test": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/test.txt",
        "clner-validation": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/validation.txt",
    },
    'TASK': "tag",
    'FULLNAME': "Chinese-Literature-NER-RE-Dataset",
    'REF': {"Source": "https://github.com/lancopku/Chinese-Literature-NER-RE-Dataset",
            "Paper": "https://arxiv.org/pdf/1711.07010.pdf"},
    'DESCRIPTION': 'We provide a new Chinese literature dataset for Named Entity Recognition (NER) and Relation Extraction (RE). We define 7 entity tags and 9 relation tags based on several available NER and RE datasets but with some additional categories specific to Chinese literature text. '
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8') as f:
        sent_input = []
        sent_target = []
        for i in list(f.readlines()):
            i = i.strip()
            if len(i) > 1:
                sent, tar = i.split(' ')
                sent_input.append(sent)
                sent_target.append(tar)
            else:
                dataset.add_data(sent_input, sent_target)
                sent_input = []
                sent_target = []
    return dataset
