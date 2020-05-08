# Copyright (C) 2019-2020 Guillermo Adrián Molina.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http:#mozilla.org/MPL/2.0/.

from oci_spec.struct import Struct
from oci_spec.digest import Digest

from datetime import datetime

StateOCIVersion = "1.0.0"

class State(Struct):
    # State holds information about the runtime state of the container.

    def __init__(
        self,
        ociVersion=None,
        id=None,
        status=None,
        pid=None,
        bundlepath=None,
        annotations=None
    ):

        super().__init__()

        # ociVersion is the version of the specification that is supported.
        self.newAttr(name="ociVersion", attType=str, required=True, jsonName="ociVersion")
        
        # ID is the container ID
        self.newAttr(name="ID", attType=str, required=True, jsonName="id")

        # Status is the runtime status of the container.
        self.newAttr(name="Status", attType=str, required=True, jsonName="status")

        # Pid is the process ID for the container process.
        self.newAttr(name="Pid", attType=int, jsonName="pid")

        # Bundle is the path to the container's bundle directory.
        self.newAttr(name="Bundle", attType=str, required=True, jsonName="bundlepath")

        # Annotations are key values associated with the container.
        self.newAttr(name="Annotations", attType=dict, jsonName="annotations")

        self.add("ociVersion", ociVersion or StateOCIVersion)
        self.add("ID", id)
        self.add("Status", status)
        self.add("Pid", pid)
        self.add("Bundle", bundlepath)
        self.add("Annotations", annotations)
