from PKB.AbstractPlugin import AbstractPlugin


class JarPlugin(AbstractPlugin):
    def generate_build_script(self, xml_dict):
        plugins = super().generate_build_script(xml_dict)
        for plugin in plugins:
            if plugin['artifactId'] == 'maven-jar-plugin':
                config = super().exists(plugin, ['configuration'])
        return config
