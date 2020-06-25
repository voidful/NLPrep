import importlib
import os
import unittest


class TestDataset(unittest.TestCase):

    def testType(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
        DATASET_DIR = os.path.join(ROOT_DIR, './datasets')
        datasets = list(filter(lambda x: os.path.isdir(os.path.join(DATASET_DIR, x)) and '__pycache__' not in x,
                               os.listdir(DATASET_DIR)))
        for dataset in datasets:
            ds = importlib.import_module('.' + dataset, 'nlprep.datasets')
            self.assertTrue(ds.TYPE in ['clas', 'tag', 'qa', 'gen'])
