import argparse
import importlib
import os

from nlprep.file_utils import cached_path
from nlprep.utils.sentlevel import *
from nlprep.utils.pairslevel import *


def getDatasets(mod, cache_dir=None):
    sets = {}
    for k, v in mod.DATASET_FILE_MAP.items():
        if isinstance(v, list):
            for i, path in enumerate(v):
                v[i] = cached_path(path, cache_dir=cache_dir)
            dataset_path = v
        else:
            dataset_path = cached_path(v, cache_dir=cache_dir)
        sets[k] = mod.toMiddleFormat(dataset_path)
    return sets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        choices=['clner', 'udicstm', 'pttgen', 'cged'])
    parser.add_argument("--task", type=str,
                        choices=['gen', 'classification', 'tagRow', 'tagCol'])
    parser.add_argument("--outdir", type=str)
    parser.add_argument("--cachedir", type=str)
    parser.add_argument("--util", type=str, nargs='+', default=[])

    global arg
    arg = parser.parse_args()

    sent_utils = [SentUtils[i] for i in arg.util if i in SentUtils]
    pairs_utils = [PairsUtils[i] for i in arg.util if i in PairsUtils]
    if not os.path.exists(arg.outdir):
        os.mkdir(arg.outdir)

    mod = importlib.import_module('.' + arg.dataset, 'nlprep.datasets')
    for k, dataset in getDatasets(mod, arg.cachedir).items():
        if arg.task == "tagRow":
            dataset.dump_tagRow(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif arg.task == "tagCol":
            dataset.dump_tagCol(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif arg.task == "gen":
            dataset.dump_gen(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif arg.task == "classification":
            dataset.dump_classification(os.path.join(arg.outdir, k), pairs_utils, sent_utils)


if __name__ == "__main__":
    main()
