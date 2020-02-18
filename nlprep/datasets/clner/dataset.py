from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "train": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/train.txt",
    "test": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/test.txt",
    "validation": "https://raw.githubusercontent.com/lancopku/Chinese-Literature-NER-RE-Dataset/master/ner/validation.txt",
}


def toMiddleFormat(path):
    dataset = MiddleFormat()
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
