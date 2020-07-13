import importlib
import os
import unittest

import nlprep
import pytest


class TestDataset(unittest.TestCase):

    def testType(self):
        datasets = nlprep.list_all_datasets()
        for dataset in datasets:
            print(dataset)
            ds = importlib.import_module('.' + dataset, 'nlprep.datasets')
            self.assertTrue("DATASETINFO" in dir(ds))
            self.assertTrue("load" in dir(ds))
            self.assertTrue(ds.DATASETINFO['TASK'] in ['clas', 'tag', 'qa', 'gen'])
