#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
OPTION 2: CREATING MOCK INSTANCES
https://www.toptal.com/python/an-introduction-to-mocking-in-python


The mock.create_autospec method creates a functionally equivalent instance to the provided class.

The mock library also includes two important classes upon which most of the internal functionality is built upon: 
mock.Mock and mock.MagicMock. 
When given a choice to use a mock.Mock instance, a mock.MagicMock instance, 
or an auto-spec, always favor using an auto-spec, 
as it helps keep your tests sane for future changes. 
This is because mock.Mock and mock.MagicMock accept all method calls and property assignments regardless of the underlying API.

"""

from unittest.mock import patch
from unittest import mock

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


def test_upload():
    # build our dependencies
    mock_removal_service = mock.create_autospec(RemovalService)
    reference = UploadService(mock_removal_service)
    
    # call upload_complete, which should, in turn, call `rm`:
    reference.upload_complete("my uploaded file")
    
    # test that it called the rm method
    mock_removal_service.rm.assert_called_with("my uploaded file")