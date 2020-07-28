from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "storyend-train": ["https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/train.post",
                           "https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/train.response"],
        "storyend-test": ["https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/test.post",
                          "https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/test.response"],
        "storyend-val": ["https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/val.post",
                         "https://raw.githubusercontent.com/JianGuanTHU/StoryEndGen/master/data/val.response"]
    },
    'TASK': "gen",
    'FULLNAME': "Five-sentence stories from ROCStories corpus ",
    'REF': {"Source": "https://github.com/JianGuanTHU/StoryEndGen",
            "ROCStories corpus": "http://cs.rochester.edu/nlp/rocstories/"},
    'DESCRIPTION': 'This corpus is unique in two ways: (1) it captures a rich set of causal and temporal commonsense relations between daily events, and (2) it is a high quality collection of everyday life stories that can also be used for story generation.'
}


def load(data):
    return data


def toMiddleFormat(paths):
    dataset = MiddleFormat(DATASETINFO)
    with open(paths[0], 'r', encoding='utf8', errors='ignore') as posts:
        with open(paths[1], 'r', encoding='utf8', errors='ignore') as resps:
            for p, r in zip(posts.readlines(), resps.readlines()):
                p = p.replace('\t', " [SEP] ").replace('\n', "")
                r = r.replace('\n', "")
                dataset.add_data(p, r)
    return dataset
