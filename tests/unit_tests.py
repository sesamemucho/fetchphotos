#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-02-22 14:17:50 bob>

## invoke tests using the call_tests.sh script in this directory

import unittest
import os
import fetchphotos
import tempfile
import os.path
import pprint
import re
import logging
from shutil import rmtree


class TestMethods(unittest.TestCase):

    def setUp(self):
        fetchphotos.initialize_logging(False, False)
        fetchphotos.fp_logger.setLevel(logging.CRITICAL)

    def test_check_getconfig(self):
        with self.assertRaisesRegexp(IOError, 'No such file or directory:'):
            c = fetchphotos.get_config_parser("hoo")

        # Make sure it works with non-ascii
        with self.assertRaises(IOError) as cm:
            c = fetchphotos.get_config_parser("«boo»")

        # We can't just use assertRaisesRegexp here because of
        # regexp+Unicode issues in the unittest regexp code.
        self.assertTrue(re.search(r'No such file or directory',
                       cm.exception.strerror))

    def test_check_tempdir(self):

        self.assertEqual(1, 1)

    def tearDown(self):

        pass

class TestConfigCheckers(unittest.TestCase):

    def setUp(self):
        fetchphotos.initialize_logging(False, False)
        fetchphotos.fp_logger.setLevel(logging.CRITICAL)
        self.cfg = fetchphotos.get_config_parser("tests/testdata/checker.cfg")

    def test_check_tempdir(self):
        with self.assertRaises(IOError) as cm:
            fetchphotos.check_tempdir(self.cfg)

        self.assertTrue(re.search(
            r'The digicam temporary directory ".*" does not exist',
            cm.exception.strerror))

    def tearDown(self):

        pass


if __name__ == '__main__':
    unittest.main()
