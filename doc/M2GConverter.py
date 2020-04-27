import os
import subprocess
import zipfile
import shutil
import importlib
from pprint import pprint

import Comparer
import POMReader
import Xml2Dict
import PKB


def build_maven(source_path):
    # mvn clean install
    os.chdir(source_path)
    subprocess.call(["mvn", "clean", "install"], shell=True)


def clear_gradle_environment(source_path):
    gradle_list = ["build.gradle", "settings.gradle", "gradle.properties"]
    for gradle_file in gradle_list:
        if gradle_file in os.listdir(source_path):
            os.remove(os.path.join(source_path, gradle_file))
    modules = POMReader.get_modules(source_path)
    for module in modules:
        clear_gradle_environment(os.path.join(source_path, module))


def convert_maven_to_gradle(source_path):
    os.chdir(source_path)
    subprocess.call(["gradle", "init", "--type", "pom"], shell=True)


def create_module_level_properties(source_path):
    POMReader.get_properties(source_path)
    modules = POMReader.get_modules(source_path)
    for module in modules:
        create_module_level_properties(os.path.join(source_path, module))


def update_gradle_scripts_with_gradle_tasks(source_path):
    root = POMReader.get_pom(source_path)
    xml_dict = Xml2Dict.XmlDictConfig(root)
    for name in PKB.__all__:
        module = importlib.import_module('PKB.' + name)
        obj = getattr(module, name)
        instance = obj()
        instance.generate_build_script(xml_dict)


def update_module_level_common_properties_reverse_map(source_path):
    pass


def generate_gradle_build_script(source_path):
    clear_gradle_environment(source_path)
    convert_maven_to_gradle(source_path)
    create_module_level_properties(source_path)
    update_gradle_scripts_with_gradle_tasks(source_path)
    update_module_level_common_properties_reverse_map(source_path)


def build_gradle(source_path):
    # gradle clean build
    os.chdir(source_path)
    subprocess.call(["gradle", "clean", "build"], shell=True)


def extract_artifact(path):
    if zipfile.is_zipfile(path):
        file, _ = os.path.splitext(path)
        if os.path.exists(file):
            shutil.rmtree(file)
        with zipfile.ZipFile(path) as z:
            z.extractall(file)
            return file


def source_destination_artifacts(source_path):
    filename_with_ext = POMReader.get_artifact_with_ext(source_path)
    if filename_with_ext:
        source_compressed_file = os.path.join(source_path, 'target/'+filename_with_ext).replace('\\', '/')
        destination_compressed_file = os.path.join(source_path, 'build/libs/'+filename_with_ext).replace('\\', '/')
        source = extract_artifact(source_compressed_file)
        destination = extract_artifact(destination_compressed_file)
        if os.path.isdir(source) and os. path.isdir(destination):
            artifact_paths = (source, destination)
            return artifact_paths
    return False


def multi_module_artifacts(source_path, sd_dict):
    modules = POMReader.get_modules(source_path)
    for module in modules:
        sd_dict[os.path.join(source_path, module).replace('\\', '/')] = \
            source_destination_artifacts(os.path.join(source_path, module).replace('\\', '/'))
    for module in modules:
        multi_module_artifacts(os.path.join(source_path, module).replace('\\', '/'), sd_dict)
    return sd_dict


def source_destination_artifact_dict(source_path):
    modules = POMReader.get_modules(source_path)
    if modules:
        return multi_module_artifacts(source_path, sd_dict={})
    else:
        sd_paths = source_destination_artifacts(source_path)
        return {source_path: sd_paths}


def compare_all_modules(sd_artifact_list):
    for module, sd_tuple in sd_artifact_list.items():
        reports = Comparer.compare(sd_tuple[0], sd_tuple[1])
        if reports:
            Comparer.save_to_csv(sd_tuple[1], reports)


def compare_one_module(sd_artifact_list, module_path):
    for module, sd_tuple in sd_artifact_list.items():
        if module_path == module:
            reports = Comparer.compare(sd_tuple[0], sd_tuple[1])
            if reports:
                Comparer.save_to_csv(sd_tuple[1], reports)


if __name__ == "__main__":
    main_path = (input("enter source path")).replace('\\', '/')
    if not os.path.isabs(main_path):
        main_path = os.path.join(os.getcwd(), main_path).replace('\\', '/')
    # build_maven(main_path)
    # clear_gradle_environment(main_path)
    # convert_maven_to_gradle(main_path)
    # create_module_level_properties(main_path)
    update_gradle_scripts_with_gradle_tasks(main_path)
    # update_module_level_common_properties_reverse_map(main_path)
    # generate_gradle_build_script(main_path)
    # build_gradle(main_path)
    # sd_list = source_destination_artifact_dict(main_path)
    # compare_all_modules(sd_list)
    # module_path = input("module path")
    # compare_one_module(sd_list, module_path)
