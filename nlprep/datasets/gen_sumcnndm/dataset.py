import os
import re

from nlprep.file_utils import cached_path
from nlprep.middleformat import MiddleFormat
import nlp2

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "cnndm-train": "train.txt",
        "cnndm-test": "test.txt",
        "cnndm-val": "val.txt"
    },
    'TASK': "gen",
    'FULLNAME': "CNN/DM Abstractive Summary Dataset",
    'REF': {"Source": "https://github.com/harvardnlp/sent-summary"},
    'DESCRIPTION': 'Abstractive Text Summarization on CNN / Daily Mail'
}


def load(data):
    import tarfile
    cache_path = cached_path("https://s3.amazonaws.com/opennmt-models/Summary/cnndm.tar.gz")
    cache_dir = os.path.abspath(os.path.join(cache_path, os.pardir))
    data_folder = os.path.join(cache_dir, 'cnndm_data')
    if nlp2.is_dir_exist(data_folder) is False:
        tar = tarfile.open(cache_path, "r:gz")
        tar.extractall(data_folder)
        tar.close()
    return [os.path.join(data_folder, data + ".src"), os.path.join(data_folder, data + ".tgt.tagged")]


REMAP = {"-lrb-": "(", "-rrb-": ")", "-lcb-": "{", "-rcb-": "}",
         "-lsb-": "[", "-rsb-": "]", "``": '"', "''": '"'}


def clean_text(text):
    text = re.sub(
        r"-lrb-|-rrb-|-lcb-|-rcb-|-lsb-|-rsb-|``|''",
        lambda m: REMAP.get(m.group()), text)
    return nlp2.clean_all(text.strip().replace('``', '"').replace('\'\'', '"').replace('`', '\''))


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    with open(path[0], 'r', encoding='utf8') as src:
        with open(path[1], 'r', encoding='utf8') as tgt:
            for ori, sum in zip(src, tgt):
                ori = clean_text(ori)
                sum = clean_text(sum)
                dataset.add_data(ori, sum)
    return dataset
