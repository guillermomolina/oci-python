# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from oci_spec.struct import Struct
from oci_spec.image.specs import Versioned
from oci_spec.logger import bot
from .mediatype import MediaTypeImageIndex, MediaTypeImageManifest
from .descriptor import Descriptor
import re


IndexSchemaVersion = 2

class Index(Struct):
    """Index references manifests for various platforms.
    This structure provides `application/vnd.oci.image.index.v1+json`
    mediatype when marshalled to JSON.
    """

    def __init__(self, manifests=None, schema_version=None, annotations=None):
        super().__init__()

        self.newAttr(name="schemaVersion", attType=Versioned, required=True)

        # Manifests references platform specific manifests.
        self.newAttr(
            name="Manifests", attType=[Descriptor], jsonName="manifests", required=True
        )

        # Annotations contains arbitrary metadata for the image index.
        self.newAttr(name="Annotations", attType=dict, jsonName="annotations")

        self.add("Manifests", manifests)
        self.add("Annotations", annotations)
        self.add("schemaVersion", schema_version or IndexSchemaVersion)

    def _validate(self):
        """custom validation function to ensure that Manifests mediaTypes
        are valid.
        """
        valid_types = [MediaTypeImageManifest, MediaTypeImageIndex]

        manifests = self.attrs.get("Manifests").value
        if manifests:
            for manifest in manifests:
                media_type = manifest.attrs.get("MediaType")
                if media_type.value not in valid_types:

                    # Case 1: it's a custom media type (allowed) but give warning
                    if media_type.validate_regexp(media_type.value):
                        bot.warning(
                            "%s is valid, but not registered." % media_type.value
                        )

                    # Case 2: not valid and doesn't match regular expression
                    else:
                        bot.error("%s is not valid for index manifest." % media_type)
                        return False

        return True
