import unittest

from nlprep.middleformat import MiddleFormat


class TestDataset(unittest.TestCase):

    DATASETINFO = {
        'DATASET_FILE_MAP': {
            "dataset_name": "dataset path"  # list for multiple detests in one tag
        },
        'TASK': ["gen", "tag", "clas", "qa"],
        'FULLNAME': "Dataset Full Name",
        'REF': {"Some dataset reference": "useful link"},
        'DESCRIPTION': 'Dataset description'
    }

    def testQA(self):
        mf = MiddleFormat(self.DATASETINFO)
        input, target = mf.convert_to_taskformat(input="okkkkkk", target=[0, 2], sentu_func=[])
        row = [input] + target if isinstance(target, list) else [input, target]
        print(row)
