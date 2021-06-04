#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

class RemovalService(object):
    """
    A service for removing objects from the filesystem.

    import rm_svc                                                                                                                                                   
    rm_ref = rm_svc.RemovalService()                                                                                                                                
    rm_ref.rm("dummy.txt") 

    """

    def rm(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)


class UploadService(object):

    def __init__(self, removal_service):
        self.removal_service = removal_service
        
    def upload_complete(self, filename):
        self.removal_service.rm(filename)