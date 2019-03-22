import urllib
import base64
import sys
import subprocess
import openshiftercommon
import refactor
import requests
import ssl


def migrate(endpoint, fromurl, tourl, fromproject, toproject, fromuser, touser, frompass, topass, sem):
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile='domain_srv.crt')
    r = urllib.request.urlopen("{}/export/{}/{}/{}/{}".format(endpoint, fromurl, fromproject, fromuser, frompass), context=sslcontext)
    f = open("_output.tgz", "wb")
    f.write(base64.b64decode(r.read()))
    f.close()
    r.close()

    refactor.refactor(fromproject, toproject)
    # Test-move operation for migrating back to the source
    # In order for this to work, deletion must precede import
    if sem == 'testmove':
        subprocess.run("oc delete all --all", shell=True)
    with open('_import.tgz', 'rb') as f:
        data = f.read()
    data = urllib.parse.quote(data)
    requests.post('{}/import/{}/{}/{}/{}'.format(endpoint, tourl, toproject, touser, topass), data=data, verify="domain_srv.crt")


def menu():
    endpoint = "https://0.0.0.0:8443"
    if len(sys.argv) == 2:
        endpoint = sys.argv[1]

    print("OpenShifter - application migration between OpenShift instances")

    names = openshiftercommon.oc_getcontexts()
    spaces = openshiftercommon.oc_getprojects(names)

    print("OpenShift names:")
    for name in names:
        for space in spaces[name]:
            print("* {} ({})".format(name, space))

    fromurl = input("Migrate from source base URL/OpenShift name: ")
    if "/" in fromurl:
        fromproject, fromurl, fromuser = fromurl.split("/")
        fromurl = fromurl.replace("-", ".")
    else:
        fromproject = input(" + source project (optional): ")
        fromuser = input(" + source username: ")
    frompass = input(" + source password: ")
    tourl = input("Migrate to target base URL/OpenShift name: ")
    if "/" in tourl:
        toproject, tourl, touser = tourl.split("/")
        tourl = tourl.replace("-", ".")
    else:
        toproject = input(" + target project (optional): ")
        touser = input(" + target username: ")
    topass = input(" + target password: ")
    sem = input("Semantics (copy/move): ")

    try:
        migrate(endpoint, fromurl, tourl, fromproject, toproject, fromuser, touser, frompass, topass, sem)
    except Exception as e:
        print("Oops - migration went wrong. Is the server running? [{}]".format(e))


menu()
