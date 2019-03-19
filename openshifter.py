from aiohttp import web
import subprocess
import json
import os
import base64
import urllib.parse
import tarfile
import glob
import makehelmchart
import openshiftercommon

OC = openshiftercommon.OC


def oc_descriptor(context, space, username, password):
	# p = subprocess.run("{} config use-context {}".format(OC, context), shell=True)
	p = subprocess.run("{} login {} --username={} --password={}".format(OC, context, username, password), shell=True)
	if p.returncode != 0:
		return
	p = subprocess.run("{} project {}".format(OC, space), shell=True)
	if p.returncode != 0:
		return
	p = subprocess.run("{} get all -o json".format(OC), shell=True, stdout=subprocess.PIPE)
	if p.returncode != 0:
		return
	return p.stdout.decode("utf-8")


def oc_volumes(json_descriptor):
	volumes = {}
	descriptor = json.loads(json_descriptor)
	for item in descriptor["items"]:
		if item["kind"] == "Pod":
			pod = item["metadata"]["name"]
			volumes[pod] = []
			containers = item["spec"]["containers"]
			for container in containers:
				volumemounts = container["volumeMounts"]
				for volumemount in volumemounts:
					volume = volumemount["mountPath"]
					volumes[pod].append(volume)
	return volumes


def oc_export(json_descriptor, volumes, context, space):
	tmpdir = os.path.join("_state", context.replace("/", "_"), space.replace("/", "_"))
	subprocess.run("rm -rf {}".format(tmpdir), shell=True)
	os.makedirs(tmpdir, exist_ok=True)

	f = open("{}/descriptor.json".format(tmpdir), "w")
	f.write(json_descriptor)
	f.close()

	for pod in volumes:
		for volume in volumes[pod]:
			os.makedirs("{}{}".format(tmpdir, volume), exist_ok=True)
			subprocess.run("{} rsync {}:{}/ {}{}".format(OC, pod, volume, tmpdir, volume), shell=True, stdout=subprocess.PIPE)
			# if p.returncode != 0:
			# 	return

	chart = makehelmchart.makehelmchart(tmpdir, volumes=True)
	# return True
	return base64.b64encode(open(chart, "rb").read()).decode("utf-8")


def oc_import(data):
	tfname = "_upload_tmp.tgz"
	tffolder = tfname + ".unpack"

	f = open(tfname, "wb")
	f.write(data)
	f.close()

	tf = tarfile.open(tfname, "r:gz")
	tf.extractall(tffolder)
	tf.close()

	firstfolder = glob.glob("{}/*".format(tffolder))[0]
	tmpdir = "{}/volumes".format(firstfolder)

	for volumearchive in glob.glob("{}/*.tgz".format(tmpdir)):
		volumefolder = volumearchive[:-4]
		tf = tarfile.open(volumearchive)
		tf.extractall(volumefolder)
		tf.close()

	subprocess.run("{} create -f {}/templates/descriptor.json".format(OC, firstfolder), shell=True)

	volumes = oc_volumes(open("{}/templates/descriptor.json".format(firstfolder)).read())

	for pod in volumes:
		for volume in volumes[pod]:
			p = subprocess.run("{} rsync {}{} {}:{}/".format(OC, tmpdir, volume, pod, volume), shell=True, stdout=subprocess.PIPE)

	return "ok, dummy"


async def api_getcontexts():
	names = openshiftercommon.oc_getcontexts()
	return web.Response(text=json.dumps(names) + "\n")


async def api_getspaces():
	names = openshiftercommon.oc_getcontexts()
	spaces = openshiftercommon.oc_getprojects(names)
	return web.Response(text=json.dumps(spaces) + "\n")


async def api_descriptor(request):
	json_descriptor = oc_descriptor(request.match_info["context"], request.match_info["space"], request.match_info["user"], request.match_info["pass"])
	return web.Response(text=json_descriptor + "\n")


async def api_volumes(request):
	json_descriptor = oc_descriptor(request.match_info["context"], request.match_info["space"], request.match_info["user"], request.match_info["pass"])
	volumes = oc_volumes(json_descriptor)
	return web.Response(text=json.dumps(volumes) + "\n")


async def api_export(request):
	ctx = request.match_info["context"]
	space = request.match_info["space"]
	username = request.match_info["user"]
	password = request.match_info["pass"]

	json_descriptor = oc_descriptor(ctx, space, username, password)
	volumes = oc_volumes(json_descriptor)
	ret = oc_export(json_descriptor, volumes, ctx, space)
	# return web.Response(text=json.dumps(ret) + "\n")
	return web.Response(text=ret)


async def api_import(request):
	ctx = request.match_info["context"]
	space = request.match_info["space"]
	username = request.match_info["user"]
	password = request.match_info["pass"]

	oc_descriptor(ctx, space, username, password)
	data = await request.read()
	data = urllib.parse.unquote_to_bytes(data.decode("utf-8"))

	# _KeysView('...')
	# data = await request.post()
	# data = str(data.keys())[11:-2]
	# data = bytes(data, "utf-8").decode("unicode_escape")
	# data = urllib.parse.unquote_to_bytes(data)

	ret = oc_import(data)
	return web.Response(text=ret)

app = web.Application()
app.add_routes([
	web.get("/spaces", api_getspaces),
	web.get("/contexts", api_getcontexts),
	web.get("/descriptor/{context}/{space}/{user}/{pass}", api_descriptor),
	web.get("/volumes/{context}/{space}/{user}/{pass}", api_volumes),
	web.get("/export/{context}/{space}/{user}/{pass}", api_export),
	web.post("/import/{context}/{space}/{user}/{pass}", api_import)
])

web.run_app(app)
