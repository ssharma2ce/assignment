# Always prefer setuptools over distutils
import atexit
import json
import os
import subprocess
import sys
from codecs import open

from setuptools import setup, find_packages
from setuptools.command.install import install

package_name = 'moe-saas-client'

with open('VERSION', encoding='utf-8') as f:
    package_version = f.read()

if os.path.exists('fury.json'):
    with open('fury.json', encoding='utf-8') as f:
        fury_json = json.load(f)
else:
    fury_json = {}

env_fury_dependencies = fury_json.get("dependencies", [])

requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', encoding='utf-8') as f:
        req_str = f.read()
        requirements = filter(lambda req: bool(req), req_str.split('\n'))

# WARN - Don't switch order here as selenium doesnt have urllib3 dependency version pinning
install_requires = env_fury_dependencies + requirements

test_dependencies = [
    'nose>=1.3.7',
    'mock>=2.0.0',
    'nose_parameterized==0.5.0',
    'nosexcover==1.0.11',
    'nose_xunitmp==0.4.0'
]


def _post_install(install_obj):
    process_args = ['moeconfget', '--package-name', install_obj.distribution.get_name()]
    is_pip_install = bool(install_obj.single_version_externally_managed)
    if is_pip_install:
        process_args.append('--pip-install')
    try:
        print subprocess.check_output(process_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        print "error code ", exc.returncode, exc.output
        sys.exit(1)


# Section to download configuration files from S3 post package install
class PackageInstall(install):
    def __init__(self, *args, **kwargs):
        install.__init__(self, *args, **kwargs)
        atexit.register(_post_install, self)


# Post Install Section Ended

print "**************************************************"
print "Installing package: " + package_name + " version: " + package_version
print "**************************************************"

setup(
    name=package_name,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=package_version,

    description='Client for %s' % package_name,
    long_description='Client for %s' % package_name,

    # The project's main homepage.
    url='https://github.com/moengage/saas/client',

    # Author details
    author='Segmentation',
    author_email='segteam@moengage.com',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Segmentation',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7'
    ],

    # What does your project relate to?
    keywords='moengage',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'scripts', 'build', 'dist']),
    package_data={
        'moengage': [],
        '': ['VERSION']
    },
    cmdclass={
        'install': PackageInstall
    },
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    tests_require=test_dependencies,

    test_suite="tests",

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['coverage']
    },
    entry_points={
        'console_scripts': [],
    },
)
