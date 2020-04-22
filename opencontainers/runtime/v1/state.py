# Copyright (C) 2019-2020 Guillermo Adrián Molina.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http:#mozilla.org/MPL/2.0/.

from opencontainers.struct import Struct
from opencontainers.digest import Digest

from datetime import datetime

class State(Struct):
    # State holds information about the runtime state of the container.

    def __init__(
        self,
        version=None,
        id=None,
        status=None,
        pid=None,
        bundle=None,
        annotations=None
    ):

        super().__init__()

        # Version is the version of the specification that is supported.
        self.newAttr(name="Version", attType=str, required=True, jsonName="ociVersion")
        
        # ID is the container ID
        self.newAttr(name="ID", attType=str, required=True, jsonName="id")

        # Status is the runtime status of the container.
        self.newAttr(name="Status", attType=str, required=True, jsonName="status")

        # Pid is the process ID for the container process.
        self.newAttr(name="Pid", attType=int, jsonName="pid")

        # Bundle is the path to the container's bundle directory.
        self.newAttr(name="Bundle", attType=str, required=True, jsonName="bundle")

        # Annotations are key values associated with the container.
        self.newAttr(name="Annotations", attType=dict, jsonName="annotations")

        self.add("Version", version)
        self.add("ID", id)
        self.add("Status", status)
        self.add("Pid", pid)
        self.add("Bundle", bundle)
        self.add("Annotations", annotations)
