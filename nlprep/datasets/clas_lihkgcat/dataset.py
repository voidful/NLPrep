import csv

from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "lihkgcat": ["https://media.githubusercontent.com/media/voidful/lihkg_dataset/master/lihkg_posts_title_cat.csv"]
    },
    'TASK': "clas",
    'FULLNAME': "LIHKG Post Title 分類資料",
    'REF': {"Source": "https://github.com/ylchan87/LiHKG_Post_NLP"},
    'DESCRIPTION': '根據title去分析屬於邊一個台'
}


def load(data):
    return data


def toMiddleFormat(paths):
    dataset = MiddleFormat(DATASETINFO)
    for path in paths:
        with open(path, encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                input = row[0]
                target = row[1]
                dataset.add_data(input.strip(), target.strip())
    return dataset
