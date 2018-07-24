import urllib.request
import base64
import sys

import openshiftercommon

def migrate(endpoint, fromurl, tourl, fromproject, toproject, fromuser, touser, frompass, topass, sem):
	r = urllib.request.urlopen("{}/export/{}/{}/{}/{}".format(endpoint, fromurl, fromproject, fromuser, frompass))
	f = open("_output.tgz", "wb")
	f.write(base64.b64decode(r.read()))
	f.close()
	r.close()

def menu():
	endpoint = "http://localhost:8080"
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
