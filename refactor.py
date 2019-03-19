import os
import tarfile
import glob
import prepare
import shutil
import sys


def refactor(source, target):
    shutil.rmtree('_importprep', ignore_errors=True)
    try:
        os.remove('_import.tgz')
    except OSError:
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


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Error: Expected 2 arguments: Source namespace, target namespace"
    refactor(sys.argv[1], sys.argv[2])
