#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'docopt',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='nohands',
    version='0.0.0',
    description="Personal finance management using WAA/FFG method.",
    long_description=readme + '\n\n' + history,
    author="Jesse Butcher",
    author_email='boweeb@gmail.com',
    url='https://jbutcher.org',
    packages=['nohands'],
    package_dir={'nohands':
                 'nohands'},
    include_package_data=True,
    install_requires=requirements,
    license="The MIT License (MIT)",
    zip_safe=False,
    keywords='nohands',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
