from nlprep.middleformat import MiddleFormat
import json
import nlp2

DATASET_FILE_MAP = {
    "dream": "https://raw.githubusercontent.com/voidful/dream_gen/master/data.csv"
}


def toMiddleFormat(path):
    dataset = MiddleFormat()
    with open(path, encoding='utf8') as f:
        for _ in list(f.readlines()):
            data = json.loads(_)
            input = nlp2.spilt_sentence_to_array(data['dream'], True)
            target = nlp2.spilt_sentence_to_array(data["decode"], True)
            if len(input) + len(target) < 512:
                input = " ".join(input)
                target = " ".join(target)
                dataset.add_data(input, target)
    return dataset
