from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    "DATASET_FILE_MAP": {
        "msraner": "https://raw.githubusercontent.com/InsaneLife/ChineseNLPCorpus/master/NER/MSRA/train1.txt",
    },
    "TASK": "tag",
    "FULLNAME": "MSRA simplified character corpora for WS and NER",
    "REF": {
        "Source": "https://github.com/InsaneLife/ChineseNLPCorpus",
        "Paper": "https://faculty.washington.edu/levow/papers/sighan06.pdf",
    },
    "DESCRIPTION": "50k+ of Chinese naming entities including Location, Organization, and Person",
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding="utf8") as f:
        for sentence in list(f.readlines()):
            sent_input = []
            sent_target = []
            word_tags = sentence.split()
            for word_tag in word_tags:
                context, tag = word_tag.split("/")
                if tag == "nr" and len(context) > 1:
                    sent_input.append(context[0])
                    sent_target.append("B-PER")
                    for char in context[1:]:
                        sent_input.append(char)
                        sent_target.append("I-PER")
                else:
                    for char in context:
                        sent_input.append(char)
                        sent_target.append("O")
            dataset.add_data(sent_input, sent_target)
    return dataset
