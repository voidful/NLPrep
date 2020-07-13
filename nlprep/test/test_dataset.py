import importlib
import os
import unittest

import pytest


class TestDataset(unittest.TestCase):

    def testType(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
        DATASET_DIR = os.path.join(ROOT_DIR, './datasets')
        datasets = list(filter(
            lambda x: os.path.isdir(os.path.join(DATASET_DIR, x)) and '__pycache__' not in x and x is not "clas_csv",
            os.listdir(DATASET_DIR)))
        for dataset in datasets:
            print(dataset)
            ds = importlib.import_module('.' + dataset, 'nlprep.datasets')
            self.assertTrue("DATASETINFO" in dir(ds))
            self.assertTrue("load" in dir(ds))
            self.assertTrue(ds.DATASETINFO['TASK'] in ['clas', 'tag', 'qa', 'gen'])
