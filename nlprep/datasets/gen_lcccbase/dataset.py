import json
import os
import re

from nlprep.file_utils import cached_path
from nlprep.middleformat import MiddleFormat
import nlp2

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "lccc-base": "https://coai-dataset.oss-cn-beijing.aliyuncs.com/LCCC-base.zip"
    },
    'TASK': "gen",
    'FULLNAME': "LCCC(Large-scale Cleaned Chinese Conversation) base",
    'REF': {"paper": "https://arxiv.org/abs/2008.03946",
            "download source": "https://github.com/thu-coai/CDial-GPT#Dataset-zh"},
    'DESCRIPTION': '我們所提供的數據集LCCC(Large-scale Cleaned Chinese Conversation)主要包含兩部分: LCCC-base 和 LCCC-large. 我們設計了一套嚴格的數據過濾流程來確保該數據集中對話數據的質量。這一數據過濾流程中包括一系列手工規則以及若干基於機器學習算法所構建的分類器。我們所過濾掉的噪聲包括：髒字臟詞、特殊字符、顏表情、語法不通的語句、上下文不相關的對話等。該數據集的統計信息如下表所示。其中，我們將僅包含兩個語句的對話稱為“單輪對話”，我們將包含兩個以上語句的對話稱為“多輪對話”。'
}


def load(data_path):
    import zipfile
    cache_path = cached_path(data_path)
    cache_dir = os.path.abspath(os.path.join(cache_path, os.pardir))
    data_folder = os.path.join(cache_dir, 'lccc_data')
    if nlp2.is_dir_exist(data_folder) is False:
        with zipfile.ZipFile(cache_path, 'r') as zip_ref:
            zip_ref.extractall(data_folder)
    path = [f for f in nlp2.get_files_from_dir(data_folder) if
            '.json' in f]
    return path


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path[0], encoding='utf8') as f:
        pairs = json.load(f)
        for pair in pairs:
            input_s = []
            for p in pair[:-1]:
                input_s.append(nlp2.join_words_to_sentence(nlp2.split_sentence_to_array(p)))
            dataset.add_data(" [SEP] ".join(input_s),
                             nlp2.join_words_to_sentence(nlp2.split_sentence_to_array(pair[-1])))
    return dataset
