"""
This file is to create serializable JSON objects, so that later on the JSON objects can be written to a JSON file
"""

from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default 
JSONEncoder.default = _default 