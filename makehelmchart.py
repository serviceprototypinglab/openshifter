import os
#import yaml
import glob
import shutil
import tarfile
import time

drmod = None
try:
	import descriptorrewriter.descriptorrewriter as drmod
except:
	pass

def makehelmchart(dirpath, volumes=False):
	helmpath = dirpath + ".helm"
	os.makedirs(os.path.join(helmpath, "templates"), exist_ok=True)

	f = open(os.path.join(helmpath, "Chart.yaml"), "w")
	print("name: {}".format(os.path.basename(dirpath)), file=f)
	print("version: 0.0.1", file=f)
	f.close()

	f = open(os.path.join(helmpath, "values.yaml"), "w")
	f.close()

	f = open(os.path.join(helmpath, "README.md"), "w")
	print("This is a dummy 'fat chart' including volumes.", file=f)
	print("Snapshot of {} at {}.".format(os.path.basename(dirpath), time.time()), file=f)
	f.close()

	descriptors = glob.glob(os.path.join(dirpath, "*.json"))
	for descriptor in descriptors:
		shutil.copy(descriptor, os.path.join(helmpath, "templates", os.path.basename(descriptor)))

	if drmod:
		dr = drmod.DescriptorRewriter()
		dirs = [os.path.join(helmpath, "templates")]
		for dirname in dirs:
			dr.scandir(dirname)
		dr.parse()

	if volumes:
		os.makedirs(os.path.join(helmpath, "volumes"), exist_ok=True)
		directories = os.listdir(dirpath)
		for directory in directories:
			if os.path.isdir(os.path.join(dirpath, directory)):
				tf = tarfile.open(os.path.join(helmpath, "volumes", directory + ".tgz"), "w:gz")
				tf.add(os.path.join(dirpath, directory))
				tf.close()

	tfpath = helmpath + ".tgz"
	tf = tarfile.open(tfpath, "w:gz")
	tf.add(helmpath, os.path.basename(dirpath) + "-chart")
	tf.close()

	return tfpath

if __name__ == "__main__":
	if drmod:
		print("DR: active")
	else:
		print("DR: inactive")
	#makehelmchart("_state/zhaw-hendu_console-appuio-ch:8443_zhaw-jspillner1/zhaw-test1")
	makehelmchart("_state/console.appuio.ch:8443/appuio-demo3922/")
