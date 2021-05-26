from my_json import JsonParser
from my_pickle import PickleParser


class ChooseSerializer:

    @staticmethod
    def choose(info):
        if info == "json":
            return JsonParser
        elif info == "pickle":
            return PickleParser
        else:
            raise Exception('Incorrect type!')