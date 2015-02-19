#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-02-22 14:17:50 bob>

## invoke tests using the call_tests.sh script in this directory

import unittest
import os
import fetchphotos
import tempfile
import os.path
from shutil import rmtree


class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_contains_tag(self):

        self.assertEqual(1, 1)

    def tearDown(self):

        pass


if __name__ == '__main__':
    unittest.main()
