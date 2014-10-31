import os

from setuptools import setup
from distutils.command.build import build
from distutils.sysconfig import get_python_lib
#from rekishi import __version__


def get_filelist(path):
    """Returns a list of all files in a given directory"""
    files = []
    directories_to_check = [path]
    while len(directories_to_check) > 0:
        current_directory = directories_to_check.pop(0)
        for i in os.listdir(current_directory):
            if i == '.gitignore':
                continue
            relative_path = current_directory + "/" + i
            if os.path.isfile(relative_path):
                files.append(relative_path)
            elif os.path.isdir(relative_path):
                directories_to_check.append(relative_path)
            else:
                print "what am i?", i
    return files

template_files = get_filelist('rekishi')
data_files = map(lambda x: x.replace('rekishi/', '', 1), template_files)

print data_files

app_name = 'rekishi'
version = '0.1'

setup(name=app_name,
    version=version,
    description='Rest API for InfluxDB filled by Shinken',
    author='Philippe Pepos Petitclerc, Thibault Cohen',
    author_email='supervision@savoirfairelinux.com',
    url='https://github.com/savoirfairelinux/rekishi',
    packages=['rekishi'],
    package_data={'rekishi': data_files},
    requires=['django', 'pynag'],
#    cmdclass=dict(build=rekishi_build),
)
