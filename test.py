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


def delete_from_list(ilist, key):
    newlist = []
    for item in ilist:
        if isinstance(item, dict):
            item = delete_keys_from_dict(item,key)
            if not item == {}:
                newlist.append(item)
        else:
            newlist.append(item)
    return newlist


def delete_keys_from_dict(obj, keys):
    #keys_set = set(keys)  # Just an optimization for the "if key in keys" lookup.

    modified_dict = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key != keys:
                if isinstance(value, (dict)):

                    modified_dict[key] = delete_keys_from_dict(value, keys)
                    #modified_dict[key] = value
                elif isinstance(value, (list)):
                    add =0
                    for item in value:
                        if not isinstance(item, (list,dict)):
                            add = 1
                    if add == 1:
                        modified_dict[key] = value
                    else:
                        newvalue = delete_from_list(value, keys)
                        if not newvalue == []:
                            modified_dict[key] = newvalue
                else:
                    modified_dict[key] = value  # or copy.deepcopy(value) if a copy is desired for non-dicts.
    elif isinstance(obj, list):

        for item in obj:
            if isinstance(item, (dict, list)):
                modified_dict.update(delete_keys_from_dict(item, keys))

    return modified_dict


#data = json.loads(open("test.json").read())
#print(delete_keys_from_dict(data,'listkey'))

def refactor(inputfile, target):

    data = json.loads(open(inputfile).read())
    source = extract_values(data,'namespace')[0]
    with fileinput.FileInput(inputfile, inplace=True) as file:
        for line in file:
            print(line.replace(source, target), end='')
    data = json.loads(open(inputfile).read())
    #data = delete_keys_from_dict(data, 'namespace')
    data = delete_keys_from_dict(data, 'host')
    #data = delete_keys_from_dict(data, 'hostIP')
    data = delete_keys_from_dict(data, 'clusterIP')
    data = delete_keys_from_dict(data, 'privileged')
    #data = delete_keys_from_dict(data, 'blockOwnerDeletion')
    #data = delete_keys_from_dict(data, 'hostPath')
    #data = delete_keys_from_dict(data, 'selfLink')
    #data = delete_keys_from_dict(data, 'env')
    #data = delete_keys_from_dict(data, "openshift.io/encoded-deployment-config")
    with open('result.json', 'w') as fp:
        json.dump(data, fp)

    os.remove(inputfile)
    os.rename('result.json', inputfile)
