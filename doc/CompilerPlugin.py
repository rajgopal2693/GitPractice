from PKB.AbstractPlugin import AbstractPlugin
from pprint import pprint
import re


class CompilerPlugin(AbstractPlugin):
    def generate_build_script(self, xml_dict):
        build_script = []
        plugins = super().generate_build_script(xml_dict)
        for plugin in plugins:
            if plugin['artifactId'] == 'maven-clean-plugin':
                build_script.append('clean {\n')
                build_script.append('}')
                config = super().exists(plugin, ['configuration'])
                if config:
                    fileset = super().exists(config, ['filesets', 'fileset'])
                    if fileset:
                        directory = super().exists(fileset, ['directory'])
                        if directory:
                            build_script.insert(1,'delete fileTree(dir:\''+directory+'\')')
                        includes = super().exists(fileset, ['includes'])
                        excludes = super().exists(fileset, ['excludes'])

                        if includes or excludes:
                            build_script.insert(2, '.matching{\n\t\t}')
                            include = super().exists(includes, ['include'])
                            exclude = super().exists(includes, ['exclude'])
                            if include:
                                if isinstance(include, str):
                                    build_script.insert(3, '\t\tinclude \''+include+'\'')
                                else:
                                    for x in include:
                                        print(build_script)
                                        build_script = build_script[:-3]+'include \'' + x + '\'\n'+build_script[-3:]
                            if exclude:
                                if isinstance(exclude, str):
                                    build_script = build_script[:-3]+'\t\texclude \'' + exclude + '\''+build_script[-3:]
                                else:
                                    for x in exclude:
                                        build_script = build_script[:-3]+'\t\texclude \'' + x + '\'\n'+build_script[-3:]
        return ''.join(build_script)
