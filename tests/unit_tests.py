#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2015-02-22 14:17:50 bob>

## invoke tests using the call_tests.sh script in this directory

import ConfigParser
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

    # Check temp dir

    def test_check_bad_tempdir(self):
        self.cfg.set(u'General', u'TEMPDIR', u'«hello»')
        with self.assertRaises(IOError) as cm:
            fetchphotos.check_tempdir(self.cfg)

        self.assertTrue(re.search(
            r'The digicam temporary directory ".*" does not exist',
            cm.exception.strerror))

    def test_check_unset_tempdir(self):
        self.cfg.set(u'General', u'TEMPDIR', u'/path-to/foo')
        with self.assertRaises(ValueError):
            fetchphotos.check_tempdir(self.cfg)

    def test_check_no_tempdir(self):
        self.cfg.remove_option(u'General', u'TEMPDIR')
        with self.assertRaises(ConfigParser.NoOptionError):
            fetchphotos.check_tempdir(self.cfg)

    def test_check_good_tempdir(self):
        self.cfg.set(u'General', u'TEMPDIR', u'./')
        fetchphotos.check_tempdir(self.cfg)
        self.assertEqual(1, 1) # No exceptions

    # Check source dir

    def test_check_bad_sourcedir(self):
        self.cfg.set(u'General', u'DIGICAMDIR', u'«hello»')
        with self.assertRaises(IOError) as cm:
            fetchphotos.check_sourcedir(self.cfg)

        self.assertTrue(re.search(
            r'The digicam photo directory ".*" does not exist',
            cm.exception.strerror))

    def test_check_unset_sourcedir(self):
        self.cfg.set(u'General', u'DIGICAMDIR', u'/path-to/foo')
        with self.assertRaises(ValueError):
            fetchphotos.check_sourcedir(self.cfg)

    def test_check_no_sourcedir(self):
        self.cfg.remove_option(u'General', u'DIGICAMDIR')
        with self.assertRaises(ConfigParser.NoOptionError):
            fetchphotos.check_sourcedir(self.cfg)

    def test_check_good_sourcedir(self):
        self.cfg.set(u'General', u'DIGICAMDIR', u'./')
        fetchphotos.check_sourcedir(self.cfg)
        self.assertEqual(1, 1) # No exceptions

    # Check destination dir 

    def test_check_bad_destdir(self):
        self.cfg.set(u'General', u'DESTINATIONDIR', u'«hello»')
        with self.assertRaises(IOError) as cm:
            fetchphotos.check_destdir(self.cfg)

        self.assertTrue(re.search(
            r'The digicam destination directory ".*" does not exist',
            cm.exception.strerror))

    def test_check_unset_destdir(self):
        self.cfg.set(u'General', u'DESTINATIONDIR', u'/path-to/foo')
        with self.assertRaises(ValueError):
            fetchphotos.check_destdir(self.cfg)

    def test_check_no_destdir(self):
        self.cfg.remove_option(u'General', u'DESTINATIONDIR')
        with self.assertRaises(ConfigParser.NoOptionError):
            fetchphotos.check_destdir(self.cfg)

    def test_check_good_destdir(self):
        self.cfg.set(u'General', u'DESTINATIONDIR', u'./')
        fetchphotos.check_destdir(self.cfg)
        self.assertEqual(1, 1) # No exceptions

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
