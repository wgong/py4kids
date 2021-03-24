#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tempfile
from unittest.mock import patch

from rm_mod import rm

@patch("rm_mod.os.path")
@patch("rm_mod.os")
def test_rm(mock_path, mock_os):
    dummy_file = "dummy.txt"

    mock_path.isfile.return_value = False

    # remove the file
    rm(dummy_file)

    assert not mock_os.remove.called

    mock_path.isfile.return_value = True

    # remove the file
    rm(dummy_file)

    assert mock_os.remove.called_with(dummy_file)
