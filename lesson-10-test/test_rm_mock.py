#!/usr/bin/env python
# -*- coding: utf-8 -*-

from myrm import rm

import unittest
from unittest.mock import patch

class RmTestCase(unittest.TestCase):

    @patch('myrm.os')        # mock os in myrm module, not os from stdlib
    def test_rm(self,mock_os):
        # remove the file
        rm("dummy path")
        # test that rm called os.remove with the right parameters
        mock_os.remove.assert_called_with("dummy path")