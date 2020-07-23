import os
import re

from nlprep.file_utils import cached_path
from nlprep.middleformat import MiddleFormat
import nlp2

DATASETINFO = {
    'DATASET_FILE_MAP': {
        # zh
        "wmt17-news-enzh-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'zh'],
        "wmt17-news-enzh-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'zh'],
        "wmt17-news-enzh-test": ["http://data.statmt.org/wmt17/translation-task/test.tgz", 'test', 'zh'],
        # cs
        "wmt17-news-encs-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'cs'],
        "wmt17-news-encs-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'cs'],
        "wmt17-news-encs-test": ["http://data.statmt.org/wmt17/translation-task/test.tgz", 'test', 'cs'],
        # de
        "wmt17-news-ende-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'de'],
        "wmt17-news-ende-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'de'],
        "wmt17-news-ende-test": ["http://data.statmt.org/wmt17/translation-task/test.tgz", 'test', 'de'],
        # es
        "wmt17-news-enes-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'es'],
        "wmt17-news-enes-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'es'],
        "wmt17-news-enes-test": ["http://data.statmt.org/wmt17/translation-task/test.tgz", 'test', 'es'],
        # fr
        "wmt17-news-enfr-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'fr'],
        "wmt17-news-enfr-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'fr'],
        # ru
        "wmt17-news-enru-train": ["http://data.statmt.org/wmt17/translation-task/training-parallel-nc-v12.tgz",
                                  'training', 'ru'],
        "wmt17-news-enru-dev": ["http://data.statmt.org/wmt17/translation-task/dev.tgz", 'dev', 'ru'],
        "wmt17-news-enru-test": ["http://data.statmt.org/wmt17/translation-task/test.tgz", 'test', 'ru'],

    },
    'TASK': "gen",
    'FULLNAME': "WMT17 NEWS TRANSLATION TASK",
    'REF': {"homepage": "http://www.statmt.org/wmt17/",
            "download source": "http://data.statmt.org/wmt17/translation-task",
            "reference preprocess": "https://github.com/twairball/fairseq-zh-en/blob/master/preprocess/prepare.py"},
    'DESCRIPTION': 'The text for all the test sets will be drawn from news articles. Participants may submit translations for any or all of the language directions. In addition to the common test sets the conference organizers will provide optional training resources.'
}


def load(data_list):
    import tarfile
    path, task, lang = data_list
    cache_path = cached_path(path)
    cache_dir = os.path.abspath(os.path.join(cache_path, os.pardir))
    data_folder = os.path.join(cache_dir, 'wmt17_data')
    task_folder = os.path.join(data_folder, task)
    if nlp2.is_dir_exist(task_folder) is False:
        tar = tarfile.open(cache_path, "r:gz")
        tar.extractall(data_folder)
        tar.close()

    pairs = [f for f in nlp2.get_files_from_dir(task_folder) if
             lang in f and 'en' in f]
    return pairs


def _preprocess_sgm(line, is_sgm):
    """Preprocessing to strip tags in SGM files."""
    if not is_sgm:
        return line
    # In SGM files, remove <srcset ...>, <p>, <doc ...> lines.
    if line.startswith("<srcset") or line.startswith("</srcset"):
        return ""
    if line.startswith("<refset") or line.startswith("</refset"):
        return ""
    if line.startswith("<doc") or line.startswith("</doc"):
        return ""
    if line.startswith("<p>") or line.startswith("</p>"):
        return ""
    # Strip <seg> tags.
    line = line.strip()
    if line.startswith("<seg") and line.endswith("</seg>"):
        i = line.index(">")
        return line[i + 1:-6]  # Strip first <seg ...> and last </seg>.


def _preprocess(line, is_sgm=False):
    line = _preprocess_sgm(line, is_sgm=is_sgm)
    line = line.replace("\xa0", " ").strip()
    return line


def _merge_blanks(src, targ, verbose=False):
    """Read parallel corpus 2 lines at a time.
    Merge both sentences if only either source or target has blank 2nd line.
    If both have blank 2nd lines, then ignore.

    Returns tuple (src_lines, targ_lines), arrays of strings sentences.
    """
    merges_done = []  # array of indices of rows merged
    sub = None  # replace sentence after merge
    with open(src, 'rb') as src_file, open(targ, 'rb') as targ_file:
        src_lines = src_file.readlines()
        targ_lines = targ_file.readlines()

        print("src: %d, targ: %d" % (len(src_lines), len(targ_lines)))
        print("=" * 30)
        for i in range(0, len(src_lines) - 1):
            s = src_lines[i].decode().rstrip()
            s_next = src_lines[i + 1].decode().rstrip()

            t = targ_lines[i].decode().rstrip()
            t_next = targ_lines[i + 1].decode().rstrip()

            if t == '.':
                t = ''
            if t_next == '.':
                t_next = ''

            if (len(s_next) == 0) and (len(t_next) > 0):
                targ_lines[i] = "%s %s" % (t, t_next)  # assume it has punctuation
                targ_lines[i + 1] = b''
                src_lines[i] = s if len(s) > 0 else sub

                merges_done.append(i)
                if verbose:
                    print("t [%d] src: %s\n      targ: %s" % (i, src_lines[i], targ_lines[i]))
                    print()

            elif (len(s_next) > 0) and (len(t_next) == 0):
                src_lines[i] = "%s %s" % (s, s_next)  # assume it has punctuation
                src_lines[i + 1] = b''
                targ_lines[i] = t if len(t) > 0 else sub

                merges_done.append(i)
                if verbose:
                    print("s [%d] src: %s\n      targ: %s" % (i, src_lines[i], targ_lines[i]))
                    print()
            elif (len(s) == 0) and (len(t) == 0):
                # both blank -- remove
                merges_done.append(i)
            else:
                src_lines[i] = s if len(s) > 0 else sub
                targ_lines[i] = t if len(t) > 0 else sub

        # handle last line
        s_last = src_lines[-1].decode().strip()
        t_last = targ_lines[-1].decode().strip()
        if (len(s_last) == 0) and (len(t_last) == 0):
            merges_done.append(len(src_lines) - 1)
        else:
            src_lines[-1] = s_last
            targ_lines[-1] = t_last

    # remove empty sentences
    for m in reversed(merges_done):
        del src_lines[m]
        del targ_lines[m]

    print("merges done: %d" % len(merges_done))
    return (src_lines, targ_lines)


def toMiddleFormat(pairs):
    dataset = MiddleFormat(DATASETINFO)
    if 'news-commentary-v12' in pairs[0]:  ## training data
        pairs = [[p, p.replace('.en', "." + re.search("v12.(.+)+-", p).group(1))] for p in pairs if '-en.en' in p]
    else:
        pairs = [[p, p.replace('src', "ref").replace(re.search("\.\w+\.", p).group(0),
                                                     "." + re.search("-\w{2}(\w{2})-", p).group(1) + ".")]
                 for p in pairs if 'src.en' in p and re.search("-\w{4}-", p)]

    for pair in pairs:
        is_sgm = 'sgm' in pair[0]
        src_lines, targ_lines = _merge_blanks(pair[0], pair[1], verbose=False)
        for src, targ in zip(src_lines, targ_lines):
            src = _preprocess(src, is_sgm)
            targ = _preprocess(targ, is_sgm)
            if len(src) > 0 and len(targ) > 0:
                dataset.add_data(src, targ)
    return dataset
