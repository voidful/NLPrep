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

    def testNormalize(self):
        mf = MiddleFormat(self.DATASETINFO)
        norm_input, norm_target = mf._normalize_input_target("fas[SEP]df", "fasdf")
        self.assertTrue("[SEP]" in norm_input)
        norm_input, norm_target = mf._normalize_input_target("我[SEP]df", "fasdf")
        self.assertTrue(len(norm_input.split(" ")) == 3)
        norm_input, norm_target = mf._normalize_input_target("how [SEP] you", "fasdf")
        self.assertTrue(len(norm_input.split(" ")) == 3)

    def testConvertToTaskFormat(self):
        mf = MiddleFormat(self.DATASETINFO)
        mf.task = 'qa'
        _, norm_target = mf.convert_to_taskformat("how [SEP] you", [3, 4], sentu_func=[])
        self.assertTrue(isinstance(norm_target, list))
