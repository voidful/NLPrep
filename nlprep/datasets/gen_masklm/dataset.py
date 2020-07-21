import re
import nlp2
import random

from tqdm import tqdm

from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'TASK': "gen"
}


def load(data):
    return data


def toMiddleFormat(path):
    from phraseg import Phraseg
    punctuations = r"[．﹑︰〈〉─《﹖﹣﹂﹁﹔！？｡。＂＃＄％＆＇（）＊＋，﹐－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.．!\"#$%&()*+,\-.\:;<=>?@\[\]\\\/^_`{|}~]+"

    dataset = MiddleFormat(DATASETINFO)
    phraseg = Phraseg(path)

    for line in tqdm(nlp2.read_files_yield_lines(path)):
        line = nlp2.clean_all(line)

        if len(nlp2.split_sentence_to_array(line)) > 1:
            phrases = list((phraseg.extract(sent=line, merge_overlap=False)).keys())
            reg = "[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]" + "|" + punctuations
            reg = "|".join(phrases) + "|" + reg
            input_sent = re.findall(reg, line, re.UNICODE)
            target_sent = re.findall(reg, line, re.UNICODE)
            for ind, word in enumerate(input_sent):
                prob = random.random()
                if prob <= 0.15:
                    input_sent[ind] = "[MASK]"
            dataset.add_data(nlp2.join_words_to_sentence(input_sent), nlp2.join_words_to_sentence(target_sent))

    return dataset
