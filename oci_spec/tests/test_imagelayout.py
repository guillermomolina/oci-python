#!/usr/bin/python

# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from oci_spec.image.v1 import ImageLayout
import os
import pytest


def test_imagelayout(tmp_path):
<<<<<<< master:opencontainers/tests/test_imagelayout.py
    """test creation of an opencontainers ImageLayout"""
=======
    """test creation of an oci_spec ImageLayout
    """
>>>>>>> Version 0.1.3:oci_spec/tests/test_imagelayout.py
    layout = ImageLayout()

    # expected faulure:  imageLayoutVersion does not match pattern or type
    with pytest.raises(SystemExit):
        layout.load({"imageLayoutVersion": 1.0})

    with pytest.raises(SystemExit):
        layout.load({"imageLayoutVersion": "1.0"})

    # valid layout
    layout.load({"imageLayoutVersion": "1.0.0"})
