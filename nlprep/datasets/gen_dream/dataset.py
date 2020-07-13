from nlprep.middleformat import MiddleFormat
import json
import nlp2

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "dream": "https://raw.githubusercontent.com/voidful/dream_gen/master/data.csv"
    },
    'TASK': "gen",
    'FULLNAME': "周公解夢資料集",
    'REF': {"Source": "https://github.com/saiwaiyanyu/tensorflow-bert-seq2seq-dream-decoder"},
    'DESCRIPTION': '透過夢境解析徵兆'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path, encoding='utf8') as f:
        for _ in list(f.readlines()):
            data = json.loads(_)
            input = nlp2.split_sentence_to_array(data['dream'], True)
            target = nlp2.split_sentence_to_array(data["decode"], True)
            if len(input) + len(target) < 512:
                input = " ".join(input)
                target = " ".join(target)
                dataset.add_data(input, target)
    return dataset
