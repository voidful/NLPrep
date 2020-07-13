from nlprep.middleformat import MiddleFormat

DATASETINFO = {
    'DATASET_FILE_MAP': {
        "dataset_name": "dataset path"  # list for multiple detests in one tag
    },
    'TASK': ["gen", "tag", "clas", "qa"],
    'FULLNAME': "Dataset Full Name",
    'REF': {"Some dataset reference": "useful link"},
    'DESCRIPTION': 'Dataset description'
}


def load(data):
    return data


def toMiddleFormat(path):
    dataset = MiddleFormat(DATASETINFO)
    # some file reading and processing
    dataset.add_data("input", "target")
    return dataset
