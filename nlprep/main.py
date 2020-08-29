import argparse
import importlib
import nlp

from nlprep.file_utils import cached_path
from nlprep.utils.sentlevel import *
from nlprep.utils.pairslevel import *

import os

os.environ["PYTHONIOENCODING"] = "utf-8"


def list_all_datasets(ignore_list=[]):
    dataset_dir = os.path.dirname(__file__) + '/datasets'
    return list(filter(
        lambda x: os.path.isdir(os.path.join(dataset_dir, x)) and '__pycache__' not in x and x not in ignore_list,
        os.listdir(dataset_dir)))


def list_all_utilities():
    return list(SentUtils.keys()) + list(PairsUtils.keys())


def load_dataset(dataset_name):
    return importlib.import_module('.' + dataset_name, 'nlprep.datasets')


def load_utilities(util_name_list, disable_input_panel=False):
    sent_utils = [SentUtils[i] for i in util_name_list if i in SentUtils]
    pairs_utils = [PairsUtils[i] for i in util_name_list if i in PairsUtils]
    # handle utility argument input
    for util_list in [pairs_utils, sent_utils]:
        for ind, util in enumerate(util_list):
            util_arg = nlp2.function_argument_panel(util, disable_input_panel=disable_input_panel)
            util_list[ind] = [util, util_arg]
    return sent_utils, pairs_utils


def convert_middleformat(dataset, input_file_map=None, cache_dir=None, dataset_arg={}):
    sets = {}
    dataset_map = input_file_map if input_file_map else dataset.DATASETINFO['DATASET_FILE_MAP']
    for map_name, map_dataset in dataset_map.items():
        loaded_dataset = dataset.load(map_dataset)
        if isinstance(loaded_dataset, list):
            for i, path in enumerate(loaded_dataset):
                loaded_dataset[i] = cached_path(path, cache_dir=cache_dir)
            dataset_path = loaded_dataset
        elif isinstance(loaded_dataset, nlp.arrow_dataset.Dataset):
            dataset_path = loaded_dataset
        else:
            dataset_path = cached_path(loaded_dataset, cache_dir=cache_dir)
        sets[map_name] = dataset.toMiddleFormat(dataset_path, **dataset_arg)
    return sets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        choices=list_all_datasets(),
                        required=True)
    parser.add_argument("--infile", type=str)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--cachedir", type=str)
    parser.add_argument("--report", action='store_true', help='dataset statistic report')
    parser.add_argument("--util", type=str, default=[], nargs='+',
                        choices=list_all_utilities())
    global arg
    arg = parser.parse_args()

    # creat dir if not exist
    nlp2.get_dir_with_notexist_create(arg.outdir)

    # load dataset and utility
    dataset = load_dataset(arg.dataset)
    sent_utils, pairs_utils = load_utilities(arg.util)

    # handle local file1
    if arg.infile:
        fname = nlp2.get_filename_from_path(arg.infile)
        input_map = {
            fname: arg.infile
        }
    else:
        input_map = None

    print("Start processing data...")
    dataset_arg = nlp2.function_argument_panel(dataset.toMiddleFormat, ignore_empty=True)
    for k, middleformat in convert_middleformat(dataset, input_file_map=input_map, cache_dir=arg.cachedir,
                                                dataset_arg=dataset_arg).items():
        middleformat.dump_csvfile(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        if arg.report:
            profile = middleformat.get_report(k)
            profile.to_file(os.path.join(arg.outdir, k + "_report.html"))


if __name__ == "__main__":
    main()
