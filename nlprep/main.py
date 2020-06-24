import argparse
import importlib
import os

import nlp
import nlp2
from nlprep.file_utils import cached_path
from nlprep.utils.sentlevel import *
from nlprep.utils.pairslevel import *
from pandas_profiling import ProfileReport
import pandas as pd
import inquirer


def getDatasets(dataset, input_file_map=None, cache_dir=None):
    sets = {}
    dataset_map = input_file_map if input_file_map else dataset.DATASET_FILE_MAP
    for k, v in dataset_map.items():
        if isinstance(v, list):
            for i, path in enumerate(v):
                v[i] = cached_path(path, cache_dir=cache_dir)
            dataset_path = v
        elif isinstance(v, nlp.arrow_dataset.Dataset):
            dataset_path = v
        else:
            dataset_path = cached_path(v, cache_dir=cache_dir)
        sets[k] = dataset.toMiddleFormat(dataset_path)
    return sets


def main():
    dataset_dir = os.path.dirname(__file__) + '/datasets'
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        choices=list(
                            filter(lambda x: os.path.isdir(os.path.join(dataset_dir, x)) and '__pycache__' not in x,
                                   os.listdir(dataset_dir))),
                        required=True)
    parser.add_argument("--infile", type=str)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--cachedir", type=str)
    parser.add_argument("--report", action='store_true', help='dataset statistic report')
    parser.add_argument("--util", type=str, default=[], nargs='+',
                        choices=list(SentUtils.keys()) + list(PairsUtils.keys()))
    global arg
    arg = parser.parse_args()

    # load dataset and utility
    sent_utils = [SentUtils[i] for i in arg.util if i in SentUtils]
    pairs_utils = [PairsUtils[i] for i in arg.util if i in PairsUtils]
    if not os.path.exists(arg.outdir):
        os.mkdir(arg.outdir)
    dataset = importlib.import_module('.' + arg.dataset, 'nlprep.datasets')

    # handle utility argument input
    for util_list in [pairs_utils, sent_utils]:
        for ind, util in enumerate(util_list):
            name = util.__name__
            if inspect.getfullargspec(util).defaults:
                arg_len = len(inspect.getfullargspec(util).args)
                def_len = len(inspect.getfullargspec(util).defaults)
                arg_w_def = zip(inspect.getfullargspec(util).args[arg_len - def_len:],
                                inspect.getfullargspec(util).defaults)
                inquirer_list = []
                for k, v in arg_w_def:
                    if isinstance(v, list):
                        msg = name + " " + k
                        inquirer_list.append(inquirer.List(k, message=msg, choices=v))
                    else:
                        if isinstance(v, float) and 0 < v < 1:  # probability
                            msg = name + " " + k + " (between 0-1)"
                        elif isinstance(v, float) or isinstance(v, int):  # number
                            msg = name + " " + k + " (number)"
                        else:
                            msg = name + " " + k
                        inquirer_list.append(inquirer.Text(k, message=msg, default=v))
                util_arg = inquirer.prompt(inquirer_list)
            else:
                util_arg = {}
            util_list[ind] = [util, util_arg]

    print("Start processing data...")
    if arg.infile:
        fname = nlp2.get_filename_from_path(arg.infile)
        input_map = {
            fname: arg.infile
        }
    else:
        input_map = None

    for k, middleformat in getDatasets(dataset, input_file_map=input_map, cache_dir=arg.cachedir).items():
        paths = middleformat.dump(os.path.join(arg.outdir, k), middleformat.Type, pairs_utils, sent_utils)
        if arg.report:
            for path in paths:
                df = pd.read_csv(path, header=None)
                profile = ProfileReport(df,
                                        html={'style': {'theme': 'flatly'}, 'minify_html': True},
                                        vars={'cat': {'unicode': True}},
                                        title=k + " report")
                path = path.replace('.csv', '')
                profile.to_file(path + "_report.html")


if __name__ == "__main__":
    main()
