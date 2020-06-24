import importlib
import os
import unittest


class TestDataset(unittest.TestCase):

    def testType(self):
        dataset_dir = '../datasets'
        datasets = list(filter(lambda x: os.path.isdir(os.path.join(dataset_dir, x)) and '__pycache__' not in x,
                               os.listdir(dataset_dir)))
        for dataset in datasets:
            ds = importlib.import_module('.' + dataset, 'nlprep.datasets')
            self.assertTrue(ds.TYPE in ['clas', 'tag', 'qa', 'gen'])
