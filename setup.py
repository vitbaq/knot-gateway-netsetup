import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="knot-gateway-netsetup",
    version="1.0",
    author="Vitor Barros",
    author_email="vba@cesar.org.br",
    description=("Netsetup Daemon"),
    license="Apache-2.0",
    keywords="daemon netsetup gateway",
    url="https://github.com/CESARBR/knot-gateway-netsetup",
    install_requires=[
        "astroid == 2.2.5"
        "autopep8 == 1.4.3"
        "dbus-python == 1.2.8"
        "docutils == 0.14"
        "isort == 4.3.15"
        "lazy-object-proxy == 1.3.1"
        "lockfile == 0.12.2"
        "mccabe == 0.6.1"
        "pep8 == 1.7.1"
        "pkg-resources == 0.0.0"
        "pycairo == 1.18.0"
        "pycodestyle == 2.5.0"
        "PyGObject == 3.32.0"
        "pylint == 2.3.1"
        "python-daemon == 2.2.3"
        "six == 1.12.0"
        "typed-ast == 1.3.1"
        "wrapt == 1.11.1"
    ],
    packages=['netsetup'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
