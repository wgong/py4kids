#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
OPTION 1: MOCKING INSTANCE METHODS
https://www.toptal.com/python/an-introduction-to-mocking-in-python

"""

from unittest.mock import patch

from rm_svc import RemovalService, UploadService

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


@patch.object(RemovalService, "rm")
def test_upload(mock_rm):
    # build our dependencies
    removal_service = RemovalService()
    reference = UploadService(removal_service)
    
    # call upload_complete, which should, in turn, call `rm`:
    reference.upload_complete("my uploaded file")
    
    # check that it called the rm method of any RemovalService
    mock_rm.assert_called_with("my uploaded file")
    
    # check that it called the rm method of _our_ removal_service
    removal_service.rm.assert_called_with("my uploaded file")