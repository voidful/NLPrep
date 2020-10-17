import json

import nlp2

from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "drcd-train": "https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_training.json",
        "drcd-test": "https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_test.json",
        "drcd-dev": "https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_dev.json",
        "cmrc-train": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/train.json",
        "cmrc-test": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/test.json",
        "cmrc-dev": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/dev.json",
        "cail-train": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/big_train_data.json",
        "cail-test": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/test_ground_truth.json",
        "cail-dev": "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/dev_ground_truth.json",
        "combine-train": ["https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_training.json",
                          "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/train.json",
                          "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/big_train_data.json"],
        "combine-test": ["https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_test.json",
                         "https://raw.githubusercontent.com/voidful/zh_mrc/master/drcd/DRCD_dev.json",
                         "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/test.json",
                         "https://raw.githubusercontent.com/voidful/zh_mrc/master/cmrc2018/dev.json",
                         "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/test_ground_truth.json",
                         "https://raw.githubusercontent.com/voidful/zh_mrc/master/cail/dev_ground_truth.json"
                         ]
    },
    'TASK': "qa",
    'FULLNAME': "多個抽取式的中文閱讀理解資料集",
    'REF': {"DRCD Source": "https://github.com/DRCKnowledgeTeam/DRCD",
            "CMRC2018 Source": "https://github.com/ymcui/cmrc2018",
            "CAIL2019 Source": "https://github.com/iFlytekJudiciary/CAIL2019_CJRC"},
    'DESCRIPTION': '有DRCD/CMRC/CAIL三個資料集'
}


def load(data):
    return data


def toMiddleFormat(paths):
    dataset = MiddleFormat(DATASETINFO)
    if not isinstance(paths, list):
        paths = [paths]

    for path in paths:
        with open(path, encoding="utf-8", errors='replace') as dataset_file:
            dataset_json = json.loads(dataset_file.read())
            dataset_json = dataset_json['data']
        for item in dataset_json:
            for paragraph in item['paragraphs']:
                for qas in paragraph['qas']:
                    question = replace_s(qas['question'])
                    for answers in qas['answers'][:1]:
                        context = replace_s(paragraph['context'])
                        ans = replace_s(str(answers['text']))
                        ori_start = start = answers['answer_start']

                        ans = nlp2.split_sentence_to_array(ans)
                        context = nlp2.split_sentence_to_array(context)
                        question = nlp2.split_sentence_to_array(question)

                        pos = -1
                        for tok in context:
                            pos += len(tok)
                            if len(tok) != 1:
                                if pos <= ori_start:
                                    start -= len(tok) - 1
                        end = start + len(ans)

                        if 'YES' in ans or 'NO' in ans:
                            input_sent = " ".join(ans + context) + " [SEP] " + " ".join(question)
                            dataset.add_data(input_sent, [0, 1])
                        elif 'FAKE' in ans:
                            input_sent = " ".join(context) + " [SEP] " + " ".join(question)
                            dataset.add_data(input_sent, [0, 0])
                        elif context[start:end] == ans:
                            input_sent = " ".join(context) + " [SEP] " + " ".join(question)
                            dataset.add_data(input_sent, [start, end])
                        else:
                            print("input_sent", context[start:end], "ans", ans)
    return dataset


def replace_s(s):
    return s.replace(" ", "_").replace("​", "_").replace('\t', "_").replace('\n', "_"). \
        replace('\r', "_").replace('\v', "_").replace('\f', "_").replace(' ', "_").replace(' ', "_").replace("　", "_")
