#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'CouchDB',
    'falcon'
]

test_requirements = [
    'ddt',
]

setup(
    name='couchdb_download_token',
    version='0.1.1',
    description="Simple web service that allows downloading CouchDB document attachments with a per-document download token.",
    long_description=readme + '\n\n' + history,
    author="Matías Lang",
    author_email='yo@matiaslang.me',
    url='https://github.com/sh4r3m4n/couchdb_download_token',
    packages=[
        'couchdb_download_token',
    ],
    package_dir={'couchdb_download_token':
                 'couchdb_download_token'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='couchdb_download_token',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
