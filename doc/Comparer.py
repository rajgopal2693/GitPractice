import os
import filecmp
import csv


def compare(source, destination):

    report = recursive_dircmp(source, destination)

    source = source.replace('\\', '/')
    destination = destination.replace('\\', '/')

    if report["left"]:
        items = []
        for item in report["left"]:
            item = item[1:]
            path = os.path.join(source, item)
            if os.path.isdir(path):
                data = list_dirs_files(path)
                items.extend(data)
        report["left"].extend(i.replace('\\', '/')[len(source):] for i in items)

    if report["right"]:
        items = []
        for item in report["right"]:
            item = item[1:]
            path = os.path.join(destination, item)
            if os.path.isdir(path):
                data = list_dirs_files(path)
                items.extend(data)
        report["right"].extend(i.replace('\\', '/')[len(destination):] for i in items)

    records = []
    files = []
    directories = []
    left_files, right_files, common_files = 0, 0, 0
    left_directories, right_directories, common_directories = 0, 0, 0

    if report["left"]:
        for item in report["left"]:
            item = item[1:]
            s_path = os.path.join(source, item).replace('\\', '/')
            record = {"Name": item, "Indicator": "<=", "Compare": "Source",
                      "SPath": s_path, "DPath": ""}
            if os.path.isfile(s_path):
                _, ext = os.path.splitext(item)
                record["FileType"] = "File"
                record["Extension"] = ext
                record["SSize"] = os.stat(record["SPath"]).st_size
                record["DSize"] = 0
                left_files += 1
                record["Result"] = "Identical" if record["SSize"] == record["DSize"] else "Not Identical"
            else:
                record["FileType"] = "Directory"
                record["Result"] = "Not Identical"
                left_directories += 1

            records.append(record)

    if report["right"]:
        for item in report["right"]:
            item = item[1:]
            d_path = os.path.join(destination, item).replace('\\', '/')
            record = {"Name": item, "Indicator": "=>", "Compare": "Destination", "SPath": "",
                      "DPath": d_path}
            if os.path.isfile(d_path):
                _, ext = os.path.splitext(item)
                record["FileType"] = "File"
                record["Extension"] = ext
                record["DSize"] = os.stat(record["DPath"]).st_size
                record["SSize"] = 0
                right_files += 1
                record["Result"] = "Identical" if record["SSize"] == record["DSize"] else "Not Identical"
            else:
                record["FileType"] = "Directory"
                record["Result"] = "Not Identical"
                right_directories += 1

            records.append(record)

    if report["both"]:
        for item in report["both"]:
            item = item[1:]
            s_path = os.path.join(source, item).replace('\\', '/')
            d_path = os.path.join(destination, item).replace('\\', '/')
            record = {"Name": item, "Indicator": "==", "Compare": "Both",
                      "SPath": s_path,
                      "DPath": d_path}
            if os.path.isfile(s_path) and os.path.isfile(d_path):
                _, ext = os.path.splitext(item)
                record["FileType"] = "File"
                record["Extension"] = ext
                record["SSize"] = os.stat(record["SPath"]).st_size
                record["DSize"] = os.stat(record["DPath"]).st_size
                common_files += 1
                record["Result"] = "Identical" if record["SSize"] == record["DSize"] else "Not Identical"
            else:
                record["FileType"] = "Directory"
                record["Result"] = "Identical"
                common_directories += 1

            records.append(record)

    files.extend((left_files, right_files, common_files))
    directories.extend((left_directories, right_directories, common_directories))

    overview(source, destination, files, directories)

    return records


def list_dirs_files(folder):

    dirs_files = []
    for root, directories, files in os.walk(folder):
        for directory in directories:
            dirs_files.append(os.path.join(root, directory))
        for file in files:
            dirs_files.append(os.path.join(root, file))
    return dirs_files


def recursive_dircmp(source, destination, prefix=''):

    comparison = filecmp.dircmp(source, destination)

    data = {
            'left': [r'{}/{}'.format(prefix, i) for i in comparison.left_only],
            'right': [r'{}/{}'.format(prefix, i) for i in comparison.right_only],
            'both': [r'{}/{}'.format(prefix, i) for i in comparison.common],
    }

    if comparison.common_dirs:
        for folder in comparison.common_dirs:
            # Compare common folder and add results to the report
            sub_source = os.path.join(source, folder)
            sub_destination = os.path.join(destination, folder)

            sub_report = recursive_dircmp(sub_source, sub_destination, (prefix + "/" + folder))
            # Add results from sub_report to main report
            for key, value in sub_report.items():
                data[key] += value

    return data


def overview(source, destination, files, directories):

    print('\nCOMPARISON OF FILES BETWEEN FOLDERS:\n')
    print('\tFOLDER 1: {}'.format(source))
    print('\tFOLDER 2: {}'.format(destination))
    print("\nFILES: " + str(sum(files)) + "\n")
    print("\tSOURCE: " + str(files[0]))
    print("\tDESTINATION: " + str(files[1]))
    print("\tBOTH: " + str(files[2]))
    print("\nFOLDERS: " + str(sum(directories)) + "\n")
    print("\tSOURCE: " + str(directories[0]))
    print("\tDESTINATION: " + str(directories[1]))
    print("\tBOTH: " + str(directories[2]))


def save_to_csv(path, items):

    fields = ['Name', 'FileType', 'Indicator', 'Compare', 'SPath', 'DPath', 'Extension', 'SSize', 'DSize', 'Result']
    filename = os.path.join(path, "reports.csv").replace('\\', '/')

    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)
