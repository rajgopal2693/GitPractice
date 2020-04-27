from abc import ABC
from pprint import pprint


class AbstractPlugin(ABC):
    def generate_build_script(self, xml_dict):
        plugins = self.exists(xml_dict, ['build', 'plugins', 'plugin'])
        if plugins:
            return plugins

    def exists(self, obj, chain):
        _key = chain.pop(0)
        if _key in obj:
            return self.exists(obj[_key], chain) if chain else obj[_key]

    def checkKey(self, xml_dict, key):
        if key in xml_dict.keys():
            print("Present, ", end=" ")
            print("value =", dict[key])
        else:
            print("Not present")
