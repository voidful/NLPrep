import unittest

from nlprep.main import *


class TestMain(unittest.TestCase):

    def testListAllDataset(self):
        self.assertTrue(isinstance(list_all_datasets(), list))

    def testListAllUtilities(self):
        self.assertTrue(isinstance(list_all_utilities(), list))

    def testLoadUtility(self):
        sent_utils, pairs_utils = load_utilities(list_all_utilities(), disable_input_panel=True)
        self.assertTrue(len(sent_utils + pairs_utils), len(list_all_utilities()))
        for func, parma in sent_utils:
            print(func, parma)
            self.assertTrue(isinstance(parma, dict))
        for func, parma in pairs_utils:
            print(func, parma)
            self.assertTrue(isinstance(parma, dict))

    def testConvertMiddleformat(self):
        mf_dict = convert_middleformat(load_dataset('clas_udicstm'))
        for mf_key, mf in mf_dict.items():
            self.assertTrue(isinstance(mf_key, str))
