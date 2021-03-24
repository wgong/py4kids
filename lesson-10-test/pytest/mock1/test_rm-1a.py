#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tempfile

from rm_mod import rm

def test_rm():
    # create a file
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
    with open(tmpfilepath, "w") as f:
        f.write("Delete me!")

    # remove the file
    rm(tmpfilepath)

    # test that it was actually removed
    assert not os.path.isfile(tmpfilepath), "Failed to remove the file."