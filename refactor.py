import os
import tarfile
import glob
import prepare
import shutil


def refactor(source, target):
    try:
        shutil.rmtree('importprep')
    except:
        pass
    try:
        os.remove('import.tgz')
    except:
        pass
    with tarfile.open('_output.tgz', 'r:gz') as tf:
        tf.extractall('importprep')
    os.chdir(glob.glob("importprep/*/templates")[0])
    prepare.prepare(source, 'descriptor.json', target)
    os.remove('descriptor.json')
    os.rename('new_descriptor.json', 'descriptor.json')
    os.chdir('../..')
    with tarfile.open('../import.tgz', 'w:gz') as tar:
        tar.add(glob.glob("*")[0])
    os.chdir('..')
    shutil.rmtree('importprep')
