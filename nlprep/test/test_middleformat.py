import unittest

from nlprep.middleformat import MiddleFormat


class TestDataset(unittest.TestCase):

    def testQA(self):
        mf = MiddleFormat('qa')
        input, target = mf.convert_to_taskformat('qa', input="okkkkkk", target=[0, 2], sentu_func=[])
        row = [input] + target if isinstance(target, list) else [input, target]
        print(row)
