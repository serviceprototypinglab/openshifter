import urllib
import base64
import sys
import subprocess
import openshiftercommon
#import refactor
import requests
import ssl
import json


def migrate(endpoint, fromurl, tourl, fromproject, toproject, fromuser, touser, frompass, topass, sem):
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile='domain_srv.crt')
    r = urllib.request.urlopen("{}/export/{}/{}/{}/{}".format(endpoint, fromurl, fromproject, fromuser, frompass),
                               context=sslcontext)
    #print(r.read())

    f = open("_output.tgz", "wb")
    f.write(base64.b64decode(r.read()))
    f.close()
    r.close()

    #refactor.refactor(fromproject, toproject)
    # Test-move operation for migrating back to the source
    # In order for this to work, deletion must precede import
    if sem == 'testmove':
        requests.get('{}/delete/{}/{}/{}/{}'.format(endpoint, fromurl, fromproject, fromuser, frompass), verify="domain_srv.crt")
    elif sem == 'fasttestmove':
        requests.get('{}/delete/{}/{}/{}/{}'.format(endpoint, tourl, toproject, touser, topass), verify="domain_srv.crt")

    with open('_output.tgz', 'rb') as f:
        data = f.read()
    data = urllib.parse.quote(data)
    requests.post('{}/import/{}/{}/{}/{}'.format(endpoint, tourl, toproject, touser, topass), data=data,
                  verify="domain_srv.crt")


def specify():
    with open("input.json", "r") as read_file:
        data = json.load(read_file)
    print("Available contexts:")
    print(list(data["credentials"]))
    choice = int(input("Your choice:"))
    context = list(data["credentials"])[choice - 1]
    return {'url': data["credentials"][context]["base"],
            'project': data["credentials"][context]["project"],
            'user': data["credentials"][context]["username"],
            'pass': data["credentials"][context]["password"]}


def menu():
    endpoint = "https://0.0.0.0:8443"
    if len(sys.argv) == 2:
        endpoint = sys.argv[1]

    print("OpenShifter - application migration between OpenShift instances")

    names = openshiftercommon.oc_getcontexts()
    spaces = openshiftercommon.oc_getprojects(names)

    print("OpenShift names:")
    for name in names:
        if name in spaces:
            for space in spaces[name]:
                print("* {} ({})".format(name, space))

    print("You can specify source (1) from file or (2) manually")
    mode = str(input("Your choice:"))
    if mode == "1":
        data = specify()
        fromurl = data["url"]
        fromproject = data["project"]
        fromuser = data["user"]
        frompass = data["pass"]
    else:
        fromurl = input("Migrate from source base URL/OpenShift name: ")
        if "/" in fromurl:
            fromproject, fromurl, fromuser = fromurl.split("/")
            fromurl = fromurl.replace("-", ".")
        else:
            fromproject = input(" + source project (optional): ")
            fromuser = input(" + source username: ")
        frompass = input(" + source password: ")

    print("You can specify target (1) from file or (2) manually")
    mode = str(input("Your choice:"))
    if mode == "1":
        data = specify()
        tourl = data["url"]
        toproject = data["project"]
        touser = data["user"]
        topass = data["pass"]
    else:
        tourl = input("Migrate to target base URL/OpenShift name: ")
        if "/" in tourl:
            toproject, tourl, touser = tourl.split("/")
            tourl = tourl.replace("-", ".")
        else:
            toproject = input(" + target project (optional): ")
            touser = input(" + target username: ")
        topass = input(" + target password: ")
    sem = input("Semantics (1) Move (2) Ping-Pong (3) Copy: ")
    if sem == "1":
        sem = "testmove"
    elif sem == "2":
        sem = "fasttestmove"

    try:
        migrate(endpoint, fromurl, tourl, fromproject, toproject, fromuser, touser, frompass, topass, sem)
    except Exception as e:
        print("Oops - migration went wrong. Is the server running? [{}]".format(e))


menu()
