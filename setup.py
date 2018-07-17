#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for networkx-neo4j
You can install networkx-neo4j with
python setup.py install
"""
import os
import sys

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (3, 6):
    print("sklearn-neo4j requires Python 3.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

packages = [
    "skneo4j",
]

if __name__ == "__main__":
    setup(
        name="sklearn-neo4j",
        version="0.0.1",
        maintainer="Mark Needham",
        maintainer_email="m.h.needham@gmal.com",
        author="Mark Needham",
        author_email="m.h.needham@gmal.com",
        description="Save sklearn models to Neo4j",
        keywords="neo4j, networkx",
        long_description="Save sklearn models to Neo4j",
        license="Apache 2",
        platforms="All",
        url="http://markhneedham.com",
        install_requires=[
            'neo4j-driver',
        ],
        packages=packages,
        zip_safe=False
    )