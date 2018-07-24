import subprocess

import os.path
OC = os.path.expanduser("~/Downloads/OpenShift/openshift-origin-client-tools-v3.9.0-191fece-linux-64bit/oc")

def oc_getcontexts():
	"""
	CURRENT   NAME                                                CLUSTER                  AUTHINFO                                 NAMESPACE
		  zhaw-hendu/console-appuio-ch:8443/zhaw-jspillner1   console-appuio-ch:8443   zhaw-jspillner1/console-appuio-ch:8443   zhaw-hendu
	*         zhaw-test1/console-appuio-ch:8443/zhaw-jspillner1   console-appuio-ch:8443   zhaw-jspillner1/console-appuio-ch:8443   zhaw-test1
	"""

	p = subprocess.run("{} config get-contexts".format(OC), shell=True, stdout=subprocess.PIPE)
	if p.returncode != 0:
		return
	lines = p.stdout.decode("utf-8").split("\n")
	if len(lines) <= 1:
		return

	names = []
	for line in lines[1:]:
		linetokens = [x for x in line.split(" ") if x]
		if len(linetokens) == 0:
			continue
		name = linetokens[0]
		if name == "*":
			name = linetokens[1]
		names.append(name)

	return names

def oc_getprojects(contexts):
	spaces = {}

	filteredcontexts = []
	for context in contexts:
		skip = False
		for filteredcontext in filteredcontexts:
			comp = context.split("/")
			filteredcomp = filteredcontext.split("/")
			if len(comp) == 3 and len(filteredcomp) == 3:
				if comp[1] == filteredcomp[1]:
					skip = True
		if not skip:
			filteredcontexts.append(context)

	for context in filteredcontexts:
		p = subprocess.run("{} config use-context {} >/dev/null".format(OC, context), shell=True)
		if p.returncode != 0:
			return
		p = subprocess.run("{} projects".format(OC), shell=True, stdout=subprocess.PIPE)
		if p.returncode != 0:
			return
		lines = p.stdout.decode("utf-8").split("\n")
		if len(lines) <= 1:
			return

		"""
		You have one project on this server: "appuio-demo3922".
		"""

		spaces[context] = []
		if lines[0].startswith("You have one project on this server"):
			spaces[context].append(lines[0].split("\"")[1])
		for line in lines[1:-2]:
			linetokens = [x for x in line.split(" ") if x]
			if len(linetokens) == 0:
				continue
			space = linetokens[0]
			if space == "*":
				space = linetokens[1]
			spaces[context].append(space)

	return spaces
