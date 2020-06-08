import argparse
import importlib
import os

from nlprep.file_utils import cached_path
from nlprep.utils.sentlevel import *
from nlprep.utils.pairslevel import *
from pandas_profiling import ProfileReport
import pandas as pd


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
    dataset_dir = os.path.dirname(__file__) + '/datasets'
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        choices=list(filter(lambda x: os.path.isdir(os.path.join(dataset_dir, x)) and "_" not in x,
                                            os.listdir(dataset_dir))),
                        required=True)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--cachedir", type=str)
    parser.add_argument("--report", action='store_true', help='dataset statistic report')
    parser.add_argument("--util", type=str, default=[], nargs='+',
                        choices=list(SentUtils.keys()) + list(PairsUtils.keys()))

    global arg
    arg = parser.parse_args()
    sent_utils = [SentUtils[i] for i in arg.util if i in SentUtils]
    pairs_utils = [PairsUtils[i] for i in arg.util if i in PairsUtils]

    if not os.path.exists(arg.outdir):
        os.mkdir(arg.outdir)

    mod = importlib.import_module('.' + arg.dataset, 'nlprep.datasets')
    for k, dataset in getDatasets(mod, arg.cachedir).items():
        if dataset.Type == "tagRow":
            dataset.dump_tagRow(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif dataset.Type == "tagCol":
            dataset.dump_tagCol(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif dataset.Type == "gen":
            dataset.dump_gen(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif dataset.Type == "classification":
            dataset.dump_classification(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        elif dataset.Type == "qa":
            dataset.dump_qa(os.path.join(arg.outdir, k), pairs_utils, sent_utils)
        df = pd.read_csv(os.path.join(arg.outdir, k), header=None)
        profile = ProfileReport(df,
                                html={'style': {'theme': 'flatly'}, 'minify_html': True},
                                vars={'cat': {'unicode': True}},
                                title=k + " report")

        profile.to_file(os.path.join(arg.outdir, k + "_report.html"))


if __name__ == "__main__":
    main()
