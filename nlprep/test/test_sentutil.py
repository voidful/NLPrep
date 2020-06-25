import importlib
import os
import unittest
import nlprep


class TestDataset(unittest.TestCase):

    def testS2T(self):
        sent_util = nlprep.utils.sentlevel
        self.assertTrue(sent_util.s2t("快乐") == "快樂")

    def testT2S(self):
        sent_util = nlprep.utils.sentlevel
        self.assertTrue(sent_util.t2s("快樂") == "快乐")
