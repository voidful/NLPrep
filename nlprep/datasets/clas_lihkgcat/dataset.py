import csv

from nlprep.middleformat import MiddleFormat

DATASET_FILE_MAP = {
    "lihkgcat": ["https://media.githubusercontent.com/media/voidful/lihkg_dataset/master/lihkg_posts_title_cat.csv"]
}
TYPE = "clas"


def toMiddleFormat(paths):
    dataset = MiddleFormat(TYPE)
    for path in paths:
        with open(path, encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                input = row[0]
                target = row[1]
                dataset.add_data(input.strip(), target.strip())
    return dataset
