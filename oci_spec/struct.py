# Copyright (C) 2019-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from oci_spec.logger import bot
from datetime import datetime
import copy
import json
import re
from dateutil import parser


class StructAttr(object):
    """A struct attribute holds a name, jsonName, value, attribute type,
    and if it's required or not. The name should hold the parameter name
    as reflected in the original (usually GoLang) implementation, while
    the jsonName is how it should be serialized to json.

    Parameters
    ==========
    name: the name (key) for the attribute
    attType: the attribute type (a python type), can be provided in list
    required: boolean if required or not
    jsonName: the name to serialize to json (not required, will use name)
    value: optionally, provide a value on init
    omitempty: if true, don't serialize with response.
    """

    def __init__(
        self,
        name,
        attType,
        required,
        jsonName=None,
        value=None,
        omitempty=True,
        regexp=None,
        hide=False,
        platform=None
    ):
        self.name = name
        self.value = value
        self.attType = attType
        self.required = required
        self.regexp = regexp or ""
        self.jsonName = jsonName or name
        self.omitempty = omitempty
        self.hide = hide
        self.platform = platform or []

    def __str__(self):
        return "<oci_spec.struct.StructAttr-%s:%s>" % (self.name, self.value)

    def __repr__(self):
        return self.__str__()

    def _is_struct(self, attType=None):
        """determine if an attType is another struct we need to populate"""
        # We can provide a nested attType to check
        if not attType:
            attType = self.attType
        try:
            return (
                Struct in attType.__bases__
                or StrStruct in attType.__bases__
                or IntStruct in attType.__bases__
            )
        except:
            return False

    def set(self, value):
        """set a new value, and validate the type. Return true if set"""
        # First pass, it might be another object to add
        # Convert it if it is not the correct type
        if self._is_struct() and not isinstance(value, self.attType):
            newStruct = self.attType()
            value = newStruct.load(value)

        # If it's a list with another type
        elif isinstance(self.attType, list) and self.attType:
            child = self.attType[0]

            # It's either a nested structure
            if self._is_struct(child):

                # If we have a list of values, generate them
                if isinstance(value, list):
                    values = []
                    for v in value:
                        # Convert it if it is not the correct type
                        if not isinstance(v, child):
                            newStruct = child()
                            v = newStruct.load(v)
                        values.append(v)
                    value = values
                else:
                    newStruct = child()
                    value = newStruct.load(value)

        # If we have a string with a regular expression
        if not self.validate_regexp(value):
            return False

        if self.attType == datetime and isinstance(value, str):
            try:
                value = parser.isoparse(value)
            except:
                return False

        if self.validate_type(value):
            self.value = value
            return True
        return False

    def to_dict(self, use_real_name=False):
        """return a dictionary representation of the attribute. This won't
        be called unless the attribute in question is a struct.
        """
        if isinstance(self.value, (str, int)):
            return self.value

        if isinstance(self.value, list):
            items = []
            for item in self.value:
                if isinstance(item, (str, int)):
                    items.append(item)
                elif isinstance(item, (Struct, StrStruct, IntStruct)):
                    items.append(item.to_dict(use_real_name))
                else:
                    items.append(item)
            return items

        return self.value.to_dict(use_real_name)

    def validate_datetime(self, value):
        """validate a datetime string, but be generous to only check day,
        month, year. This is a road nobody wants to go down.
        """
        value = value.split("T")[0]
        try:  # "2015-10-31T22:22:56.015925234Z"
            parser.isoparse(value)
            return True
        except ValueError:
            return False

    def validate_regexp(self, value):
        """validate a string or nested string values against a regular
        expression. Return True if valid or not applicable, False otherwise
        """
        if not self.regexp:
            return True

        # Only need to look at immediate children
        if not isinstance(value, list):
            value = [value]

        for entry in value:
            if isinstance(entry, str):
                if not re.search(self.regexp, entry):
                    bot.error("%s failed regex validation %s " % (entry, self.regexp))
                    return False
        return True

    def validate_type(self, value):
        """ensure that an attribute is of the correct type. If we are given
        a list as type, then the value within it is the type we are checking.
        """
        # If it's a list with something inside
        if isinstance(self.attType, list):

            # If value not a list, invalid
            if not isinstance(value, list):
                return False

            # A type to check is inside
            if self.attType:
                attType = self.attType[0]
                for entry in value:
                    if not isinstance(entry, attType):
                        return False

        # If it's a datetime, should be valid string
        elif self.attType == datetime and isinstance(value, str):
            return self.validate_datetime(value)

        # Otherwise, validate as is
        else:
            if not isinstance(value, self.attType):
                return False
        return True


class Struct(object):
    """a Struct is a general base class that allows for printing
    and validating a set of attributes according to their defined subclass.
    the subclass should have an init function that uses the functions
    here to add required attributes.
    """

    @classmethod
    def from_json(cls, data_json):
        obj = cls()
        obj.load(data_json)
        return obj

    @classmethod
    def read(cls, file_pointer):
        file_json = json.load(file_pointer)
        return cls.from_json(file_json)

    @classmethod
    def from_file(cls, file_name):
        with open(file_name, 'r') as file_pointer:
            return cls.read(file_pointer)

    def __init__(self):
        self.attrs = {}

    def newAttr(
        self,
        name,
        attType,
        required=False,
        jsonName=None,
        omitempty=True,
        regexp="",
        hide=False,
        platform=None
    ):
        """add a new attribute, including a name, json key to dump,
        type, and if required. We don't need a value here. You can
        also update a current attribute here.

        Parameters
        ==========
        name: the name (key) for the attribute
        attType: the attribute type (a python type), can be provided in list
        required: boolean if required or not
        jsonName: the name to serialize to json (not required, will use name)
        omitempty: if true, don't serialize with response.
        regexp: if a string is provided as the type (or nested), check against
        """
        self.attrs[name] = StructAttr(
            name=name,
            attType=attType,
            required=required,
            jsonName=jsonName,
            omitempty=omitempty,
            regexp=regexp,
            hide=hide,
            platform=platform
        )

    def _clear_values(self):
        """if a load is done, we remove previously loaded values for any
        attributes
        """
        for name, att in self.attrs.items():
            self.attrs[name].value = None

    def to_dict(self):
        """return a Struct as a dictionary, must be valid"""
        # A lookup of "empty" values based on types (mirrors Go)
        lookup = {str: "", int: None, list: [], dict: {}}

        # import code
        # code.interact(local=locals())

        if self.validate():
            result = {}
            for name, att in self.attrs.items():

                # Don't show if unset and omit empty, OR marked to hide
                if (att.value is None and att.omitempty) or att.hide:
                    continue
                if att.value is None:
                    value = lookup.get(att.attType, [])
                else:
                    # If structure or list, call to_dict
                    if att._is_struct() or isinstance(att.value, list):
                        value = att.to_dict(use_real_name)
                    elif isinstance(att.value, datetime):
                        value = att.value.strftime('%Y-%m-%dT%H:%M:%S.%f000Z')
                    else:
                        value = att.value
                name = att.jsonName
                if use_real_name:
                    name = att.name
                result[name] = value
            return result

    def to_json(self):
        """get the dictionary of a struct and return pretty printed json"""
        result = self.to_dict()
        if result:
            if compact:
                result = json.dumps(result, separators=(',', ':'))
            else: 
                result = json.dumps(result, indent=4)
        return result
    
    def write(self, file_ptr, compact=True):
        result = self.to_json(compact)
        if result:
            file_ptr.write(result)
    
    def save(self, file_name, compact=True):
        with open(file_name, 'w') as file_ptr:
            self.write(file_ptr, compact)

    def get(self, name):
        """get a value from an existing attribute, normally when used by a client
        """

        if name not in self.attrs:
            bot.exit("%s is not a valid attribute." % name)

        attr = self.attrs[name]

        # Don't show if unset and omit empty, OR marked to hide
        if (not attr.value and attr.omitempty) or attr.hide:
            return None

        return attr.value

    def add(self, name, value):
        """add a value to an existing attribute, normally when used by a client"""
        if name not in self.attrs:
            bot.exit("%s is not a valid attribute." % name)

        attr = self.attrs[name]

        # Don't validate the type if provided is empty
        if value:
            if not attr.set(value):
                bot.exit("%s must be type %s." % (name, attr.attType))

    def load(self, content, validate=True):
        """given a dictionary load into its respective object
        if validate is True, we require it to be completely valid.
        """
        # import code
        # code.interact(local=locals())

        if not isinstance(content, dict):
            bot.exit("Please provide a dictionary or list to load.")

        # Look up attributes based on jsonKey
        lookup = self.generate_json_lookup()

        for key, value in content.items():
            att = lookup.get(key)
            if not att:
                bot.exit("%s is not a valid json attribute." % key)

        # If we get here, all parameters are valid, replace
        self._clear_values()

        for key, value in content.items():
            att = lookup.get(key)
            valid = att.set(value)
            if not valid and validate:
                bot.exit("%s (%s) is not valid." % (att.name, att.jsonName))

        # Validate the entire structure
        if validate:
            if not self.validate():
                bot.exit("%s is invalid" % self)
        return self

    def generate_json_lookup(self):
        """based on the attributes, generate a jsonName lookup object.
        keys are jsonNames we find in the wild, names are attribute names.
        """
        lookup = dict()
        for name, att in self.attrs.items():
            lookup[att.jsonName] = att
        return lookup

    def validate(self):
        """validate goes through each attribute, and ensure that it is of the
        correct type, and if required it is defined. This is already done
        to some extent when load is called, but this function serves as
        a final validation (after an initial config is loaded).
        """
        for name, att in self.attrs.items():

            # Not required, undefined
            if not att.required and not att.value:
                continue

            '''# A required attribute cannot be None
            if att.required and att.value is None:
                bot.error("%s is required." % name)
                return False'''

            # A required attribute cannot be empty unless omitempty is False
            if att.required and not att.value and att.omitempty:
                bot.error("%s is required." % name)
                return False

            # The attribute must match its type
            if not att.validate_type(att.value):
                bot.error("%s should be type %s" % (name, att.attType))
                return False

        # Some structs need to further validate string content
        if hasattr(self, "_validate"):
            if not self._validate():
                return False
        return True
    
    def save_json(self, file_name, compact=True):
        result = self.to_json(compact)
        if result is not None:
            with open(file_name, 'w') as f:
                f.write(result)



class StrStruct(Struct, str):
    """a string Struct provides (generally) the same functions, but isn't
    tied to attributes but rather a single string value.
    """

    def __init__(self, value, **kwargs):
        self.value = value or ""
        super().__init__(**kwargs)

    def load(self, content, validate=True):
        # If we have a string, self must also have string subclass
        if isinstance(self, str) and isinstance(content, str):
            self = self.__class__(content)
            self.validate()
            return self


class IntStruct(Struct, int):
    """a string Struct provides (generally) the same functions, but isn't
    tied to attributes but rather a single string value.
    """

    def __init__(self, value, **kwargs):
        self.value = value or ""
        super().__init__(**kwargs)

    def load(self, content, validate=True):
        # If we have an int, self must also have int subclass
        if isinstance(self, int) and isinstance(content, int):
            self = self.__class__(content)
            self.validate()
            return self