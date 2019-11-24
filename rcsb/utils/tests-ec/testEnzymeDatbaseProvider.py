##
# File:    EnzymeDatabaseProviderTests.py
# Author:  J. Westbrook
# Date:    3-Feb-2019
# Version: 0.001
#
# Update:
#
#
##
"""
Tests for various utilities for extracting data from Enzyme Database
export data files.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import shutil
import unittest

from rcsb.utils.ec.EnzymeDatabaseProvider import EnzymeDatabaseProvider

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


class EnzymeDatabaseProviderTests(unittest.TestCase):
    def setUp(self):
        self.__dirPath = os.path.join(os.path.dirname(TOPDIR), "rcsb", "mock-data")
        self.__workPath = os.path.join(HERE, "test-output")
        # Maintain local copy of data file as url data source is unreliable.
        self.__ecFilePath = os.path.join(HERE, "test-data", "enzyme-data.xml.gz")
        shutil.copyfile(self.__ecFilePath, os.path.join(self.__workPath, "enzyme-data.xml.gz"))
        #
        if os.path.exists(os.path.join(self.__workPath, "enzyme-data.json")):
            os.remove(os.path.join(self.__workPath, "enzyme-data.json"))

    def tearDown(self):
        pass

    def testReloadEnzymeDatabase1(self):
        """ Test load from source
        """
        edbu = EnzymeDatabaseProvider(enzymeDirPath=self.__workPath, useCache=True)
        ecId = "1.2.3.4"
        cl = edbu.getClass(ecId)
        self.assertEqual(cl, "oxalate oxidase")
        logger.debug("ecId %s class %r", ecId, cl)
        linL = edbu.getLineage("1.2.3.4")
        self.assertEqual(len(linL), 4)
        logger.debug("ecId %s lineage (%d) %r", ecId, len(linL), linL)
        #
        idTupL = [("1.-.-.-", "1"), ("1.-", "1"), ("1.2.-.-", "1.2"), ("1.2.3.-", "1.2.3"), ("1.2..", "1.2")]
        for idIn, idOut in idTupL:
            tId = edbu.normalize(idIn)
            self.assertEqual(tId, idOut)
            linL = edbu.getLineage(tId)
            self.assertGreaterEqual(len(linL), 1)
        #

    def testReloadEnzymeDatabase2(self):
        """ Test load from cache
        """
        edbu = EnzymeDatabaseProvider(enzymeDirPath=self.__workPath, useCache=True)
        ecId = "1.2.3.4"
        cl = edbu.getClass(ecId)
        self.assertEqual(cl, "oxalate oxidase")
        logger.debug("ecId %s class %r", ecId, cl)
        linL = edbu.getLineage("1.2.3.4")
        self.assertEqual(len(linL), 4)
        logger.debug("ecId %s lineage (%d) %r", ecId, len(linL), linL)
        treeL = edbu.getTreeNodeList()
        logger.info("treeL length is %d", len(treeL))
        ecId = "5.6.2.3"
        linL = edbu.getLineage(ecId)
        self.assertEqual(linL, None)
        ecId = "7.6.2.16"
        cl = edbu.getClass(ecId)
        self.assertEqual(cl, "ABC-type putrescine transporter")


def readEnzymeDatabase():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(EnzymeDatabaseProviderTests("testReloadEnzymeDatabase1"))
    suiteSelect.addTest(EnzymeDatabaseProviderTests("testReloadEnzymeDatabase2"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = readEnzymeDatabase()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
