import importlib
import os
import unittest
import nlprep


class TestDataset(unittest.TestCase):

    def testReverse(self):
        pair_util = nlprep.utils.pairslevel
        dummyPath = "path"
        dummyPair = [["a", "b"]]
        rev_pair = pair_util.reverse(dummyPath, dummyPair)[0][1]
        dummyPair.reverse()
        self.assertTrue(rev_pair == dummyPair)

    def testSplitData(self):
        pair_util = nlprep.utils.pairslevel
        dummyPath = "path"
        dummyPair = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10]]

        splited = pair_util.splitData(dummyPath, dummyPair, train_ratio=0.7, test_ratio=0.2, valid_ratio=0.1)
        print(splited)
        for s in splited:
            if "train" in s[0]:
                self.assertTrue(len(s[1]) == 7)
            elif "test" in s[0]:
                self.assertTrue(len(s[1]) == 2)
            elif "valid" in s[0]:
                self.assertTrue(len(s[1]) == 1)

    def testSetSepToken(self):
        pair_util = nlprep.utils.pairslevel
        dummyPath = "path"
        dummyPair = [["a [SEP] b", "c"]]
        processed = pair_util.setSepToken(dummyPath, dummyPair, sep_token="QAQ")
        print(processed[0][1][0])
        self.assertTrue("QAQ" in processed[0][1][0][0])

    def testSetMaxLen(self):
        pair_util = nlprep.utils.pairslevel
        dummyPath = "path"
        dummyPair = [["a" * 513, "c"]]
        processed = pair_util.setMaxLen(dummyPath, dummyPair, maxlen=512, tokenizer="char",
                                        with_target=False, handle_over='remove')
        self.assertTrue(0 == len(processed[0][1]))
        processed = pair_util.setMaxLen(dummyPath, dummyPair, maxlen=512, tokenizer="char",
                                        with_target=False, handle_over='slice')
        self.assertTrue(len(processed[0][1][0][0]) < 512)
        processed = pair_util.setMaxLen(dummyPath, dummyPair, maxlen=514, tokenizer="char",
                                        with_target=True, handle_over='remove')
        self.assertTrue(0 == len(processed[0][1]))

    def testsplitDataIntoPart(self):
        pair_util = nlprep.utils.pairslevel
        dummyPath = "path"
        dummyPair = [["a", "b"]] * 10
        processed = pair_util.splitDataIntoPart(dummyPath, dummyPair, part=4)
        print(processed)
