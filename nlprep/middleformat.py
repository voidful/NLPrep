import csv
from tqdm import tqdm
import nlp2

from pandas_profiling import ProfileReport
import pandas as pd

# {
#     "input": [
#         example1 input,
#         example2 input,
#         ...
#     ],
#     "target": [
#         example1 target,
#         example2 target,
#         ...
#     ]
# }
from nlprep.utils.pairslevel import separate_token


class MiddleFormat:

    def __init__(self, dataset_info):
        self.pairs = []
        self.processed_pairs = []

        self.task = dataset_info['TASK']
        self.file_map = dataset_info.get('DATASET_FILE_MAP', {})
        self.fullname = dataset_info.get('FULLNAME', "")
        self.ref = dataset_info.get('REF', "")
        self.desc = dataset_info.get('DESCRIPTION', "")

    def add_data(self, input, target):
        self.pairs.append([input, target])

    def _run_pair_utility(self, path, pairsu_func=[]):
        processed_pair = []
        if len(pairsu_func) > 0:
            for func_pack in pairsu_func:
                func, func_arg = func_pack
                if len(processed_pair) > 0:
                    new_pp = []
                    for pp in processed_pair:
                        path, pairs = pp
                        new_pp.extend(func(path, pairs, **func_arg))
                    processed_pair = new_pp
                else:
                    processed_pair = func(path, self.pairs, **func_arg)
        else:
            processed_pair = [[path, self.pairs]]
        return processed_pair

    def _run_sent_utility(self, sents, sentu_func=[]):
        for ind, sent in enumerate(sents):
            for func, func_arg in sentu_func:
                sents[ind] = func(sent, **func_arg)
        return sents

    def _normalize_input_target(self, input, target=None):

        if isinstance(input, str) and not nlp2.is_all_english(input):
            split_sep_tok = " ".join(nlp2.split_sentence_to_array(separate_token))
            input = " ".join(nlp2.split_sentence_to_array(input)).replace(split_sep_tok, separate_token)

        if isinstance(target, str) and not nlp2.is_all_english(target):
            target = " ".join(nlp2.split_sentence_to_array(target))

        if isinstance(input, list):
            input = " ".join(input)
        if isinstance(target, list):
            target = " ".join(target)

        return input, target

    def convert_to_taskformat(self, input, target, sentu_func):
        if self.task == "tag":
            input, target = self._normalize_input_target(input, target)
            input = self._run_sent_utility([input], sentu_func)[0]
        elif self.task == "gen":
            input, target = self._normalize_input_target(input, target)
            input, target = self._run_sent_utility([input, target], sentu_func)
        elif self.task == "clas":
            input, target = self._normalize_input_target(input, target)
            input, target = self._run_sent_utility([input, target], sentu_func)
        elif self.task == "qa":
            input, _ = self._normalize_input_target(input)
            input = self._run_sent_utility([input], sentu_func)[0]
        return input, target

    def dump_list(self, pairsu_func=[], sentu_func=[], path=''):
        self.processed_pairs = []
        processed_pair = self._run_pair_utility(path, pairsu_func)
        for pp in processed_pair:
            path, pairs = pp
            result_list = []
            for input, target in tqdm(pairs):
                input, target = self.convert_to_taskformat(input, target, sentu_func)
                res = [input] + target if isinstance(target, list) else [input, target]
                result_list.append(res)
            yield path, result_list
            self.processed_pairs.extend(result_list)

    def dump_csvfile(self, path, pairsu_func=[], sentu_func=[]):
        for dump_path, dump_pairs in self.dump_list(pairsu_func=pairsu_func, sentu_func=sentu_func, path=path):
            with open(dump_path + ".csv", 'w', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(dump_pairs)

    def get_report(self, report_name):
        if len(self.processed_pairs) == 0:
            [_ for _ in self.dump_list()]
        df = pd.DataFrame(self.processed_pairs)

        df.columns = ['input'] + ['target_' + str(i) for i in range(len(df.columns) - 1)] \
            if len(df.columns) > 2 else ['input', 'target']
        profile = ProfileReport(df,
                                html={'style': {'primary_color': '#999999', 'full_width': True}, 'minify_html': True},
                                vars={'cat': {'unicode': True}},
                                title=report_name + " report")
        return profile
