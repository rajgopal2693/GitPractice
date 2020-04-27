import xml.etree.ElementTree as Et
import os
import re


def get_pom(pom_file_path_dir):
    pom_file = os.path.join(pom_file_path_dir, 'pom.xml')
    if os.path.exists(pom_file):
        with open(pom_file) as f:
            xml_string = f.read()
        xml_string = re.sub('\\sxmlns="[^"]+"', '', xml_string, count=1)
        root = Et.fromstring(xml_string)
        return root


def get_artifact_with_ext(pom_file_path_dir):
    pom_obj = get_pom(pom_file_path_dir)
    ext = ''
    if pom_obj.find('packaging').text != 'pom':
        ext = pom_obj.find('packaging').text
    name = pom_obj.find('artifactId').text
    try:
        version = pom_obj.find('parent/version').text
    except:
        version = pom_obj.find('version').text
    if ext:
        return name + "-" + version + "." + ext


def get_modules(pom_file_path_dir):
    pom_obj = get_pom(pom_file_path_dir)
    modules = []
    for module in pom_obj.findall('modules/module'):
        modules.append(module.text.strip())
    return modules


def get_properties(pom_file_path_dir):
    pom_obj = get_pom(pom_file_path_dir)
    for child in pom_obj.findall('properties'):
        with open(os.path.join(pom_file_path_dir, 'gradle.properties'), 'w') as gp:
            for properties in child:
                gp.write(properties.tag.replace('.', '_') + " = " + properties.text.strip() + "\n")
