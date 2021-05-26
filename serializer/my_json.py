from serialize import dumps as _dumps
from serialize import dump as _dump
from serialize import loads as _loads
from serialize import load as _load


class JsonParser:

    def dumps(self, value_indent, value_sort):
        return _dumps(self, value_indent, value_sort)

    def loads(self):
        return _loads(self)

    def dump(self, fp, value_indent, value_sort):
        return _dump(self, fp, value_indent, value_sort)

    def load(self):
        return _load(self)