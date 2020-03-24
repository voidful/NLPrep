import re
import string

from nlprep.middleformat import MiddleFormat
import gzip
import json
from tqdm import tqdm

DATASET_FILE_MAP = {
    "train": ["https://multiqa.s3.amazonaws.com/squad2-0_format_data/SQuAD2-0_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/NewsQA_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/HotpotQA_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/TriviaQA_wiki_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/SearchQA_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/BoolQ_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComplexWebQuestions_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DROP_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/WikiHop_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DuoRC_Paraphrase_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DuoRC_Self_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComplexQuestions_train.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComQA_train.json.gz"],
    "valid": ["https://multiqa.s3.amazonaws.com/squad2-0_format_data/NewsQA_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/HotpotQA_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/TriviaQA_unfiltered_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/TriviaQA_wiki_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/SearchQA_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/BoolQ_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComplexWebQuestions_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DROP_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/WikiHop_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DuoRC_Paraphrase_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/DuoRC_Self_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComplexQuestions_dev.json.gz",
              "https://multiqa.s3.amazonaws.com/squad2-0_format_data/ComQA_dev.json.gz"]
}
DATASET_FILE_MAP = {
    "valid": ["https://multiqa.s3.amazonaws.com/squad2-0_format_data/DROP_dev.json.gz"]
}


def _normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def toMiddleFormat(paths):
    dataset = MiddleFormat()

    miss = 0
    total = 0

    for path in paths:
        with gzip.open(path, "rb") as f:
            data = json.loads(f.read())
            data = data["data"][0]["paragraphs"]
            for i in tqdm(data):
                for qas in i["qas"]:
                    q = qas['question']
                    if len(qas['answers']) == 0:
                        continue
                    ans = qas['answers'][0]
                    ans_text = ans['text']
                    start = int(ans['answer_start'])
                    end = start + len(ans_text)
                    input = i["context"] + " [SEP] " + q

                    total += 1
                    if len(input.split(" ")) > 500:
                        miss += 1
                        continue

                    tag = ["O"] * len(input)
                    tag[start:end] = ["A"] * len(ans_text)
                    tag_pos = [0] * len(input)

                    pos = 0
                    token = ""
                    input_token = []
                    for char_i, char in enumerate(input):
                        tag_pos[char_i] = pos
                        token += char
                        if char is " ":
                            pos += 1
                            input_token.append(token)
                            token = ""

                    start_lock = False
                    for tok in zip(tag_pos, tag):
                        ans_pos, is_ans = tok
                        if is_ans == "A" and not start_lock:
                            start = ans_pos
                            start_lock = True
                        elif is_ans == "A":
                            end = ans_pos + 1
                    input = input_token

                    if _normalize_answer(" ".join(input[start:end])) != _normalize_answer(ans_text):
                        miss += 1
                    else:
                        dataset.add_data(input, [start, end])

    print("over:", miss, 'total:', total, 'rate:', miss / total)
    return dataset
