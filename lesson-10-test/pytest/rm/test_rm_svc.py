#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from rm_svc import RemovalService, UploadService

@patch("rm_svc.os.path")
@patch("rm_svc.os")
def test_rm(mock_os, mock_os_path):
    dummy_file = "dummy.txt"
    rm_ref = RemovalService()

    mock_os_path.isfile.return_value = False
    # remove the file
    rm_ref.rm(dummy_file)
    assert not mock_os.remove.called

    mock_os_path.isfile.return_value = True
    # remove the file
    rm_ref.rm(dummy_file)
    assert mock_os.remove.called_with(dummy_file)


def test_upload():
    # build our dependencies
    mock_removal_service = unittest.mock.create_autospec(RemovalService)
    reference = UploadService(mock_removal_service)
    
    # call upload_complete, which should, in turn, call `rm`:
    reference.upload_complete("my uploaded file")
    
    # test that it called the rm method
    mock_removal_service.rm.assert_called_with("my uploaded file")