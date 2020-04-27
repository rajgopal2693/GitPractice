import PKB.CompilerPlugin as cp
import importlib
import Xml2Dict
import POMReader
from pprint import pprint


root = POMReader.get_pom('')
xml_dict = Xml2Dict.XmlDictConfig(root)
k = cp.CompilerPlugin()
print(k.generate_build_script(xml_dict))
'''for name in PKB.__all__:
    module = importlib.import_module('PKB.'+name)
    obj = getattr(module, name)
    instance = obj()
    pprint(instance.generate_build_script(xml_dict))
    # instance.generate_script()
    

clean {
	delete fileTree(dir:'.').matching{
		include '**/*.tmp'
		include '**/*.log'
		exclude '**/important.log'
		exclude '**/another-important.log'
	}
}
'''


