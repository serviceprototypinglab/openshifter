import os
import tarfile
import glob
import prepare
import shutil


def refactor(source, target):
    try:
        shutil.rmtree('_importprep')
    except:
        pass
    try:
        os.remove('_import.tgz')
    except:
        pass
    with tarfile.open('_output.tgz', 'r:gz') as tf:
        tf.extractall('_importprep')
    os.chdir(glob.glob("_importprep/*/templates")[0])
    prepare.prepare(source, 'descriptor.json', target)
    os.remove('descriptor.json')
    os.rename('new_descriptor.json', 'descriptor.json')
    os.chdir('../..')
    with tarfile.open('../_import.tgz', 'w:gz') as tar:
        tar.add(glob.glob("*")[0])
    os.chdir('..')
    shutil.rmtree('_importprep')
