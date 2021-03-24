#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch

from rm_svc import RemovalService

@patch("rm_svc.os.path")
@patch("rm_svc.os")
def test_rm(mock_path, mock_os):
    dummy_file = "dummy.txt"

    rm_ref = RemovalService()

    mock_path.isfile.return_value = False

    # remove the file
    rm_ref.rm(dummy_file)

    assert not mock_os.remove.called

    mock_path.isfile.return_value = True

    # remove the file
    rm_ref.rm(dummy_file)

    assert mock_os.remove.called_with(dummy_file)
