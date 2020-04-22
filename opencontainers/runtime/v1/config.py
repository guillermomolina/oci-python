# Copyright (C) 2019-2020 Guillermo Adrián Molina.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http:#mozilla.org/MPL/2.0/.

from opencontainers.struct import Struct
from opencontainers.digest import Digest

from datetime import datetime

class User(Struct):
    # User specifies specific user (and group) information for the container process.

    def __init__(
        self,
        umask=None,
        additionalGids=None,
        username=None
    ):

        super().__init__()

        # UID is the user id.
        self.newAttr(name="UID", attType=int, required=True, jsonName="uid", platform="linux,solaris")

        # GID is the group id.
        self.newAttr(name="GID", attType=int, required=True, jsonName="gid", platform="linux,solaris")

        # Umask is the umask for the init process.
        self.newAttr(name="Umask", attType=int, jsonName="umask", platform="linux,solaris")

        # Umask is the umask for the init process.
        self.newAttr(name="AdditionalGids", attType=[int], jsonName="additionalGids", platform="linux,solaris")

        # Username is the user name.
        self.newAttr(name="Username", attType=str, jsonName="username", platform="windows")

        self.add("UID", uid)
        self.add("GID", gid)
        self.add("Umask", umask)
        self.add("AdditionalGids", additionalGids)
        self.add("Username", username)
