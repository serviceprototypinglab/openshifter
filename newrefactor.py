import os
import fileinput
import json


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def refactor(inputfile, target):

    data = json.loads(open(inputfile).read())
    source = extract_values(data,'namespace')[0]
    with fileinput.FileInput(inputfile, inplace=True) as file:
        for line in file:
            print(line.replace(source, target), end='')

    with open(inputfile) as oldfile, open('new_descriptor.json', 'w') as newfile:
        for line in oldfile:
            if not ('"host"' in line) and not ('"clusterIP"' in line) and not ('"privileged":' in line):
                newfile.write(line)
    os.remove(inputfile)
    os.rename('new_descriptor.json', inputfile)

#refactor('test.json', 'myproject')
