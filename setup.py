#!/usr/bin/env python3

from setuptools import setup

with open('README.rst') as fin:
    description = fin.read()

setup(
    name='confucius',
    version='1.0.3',
    description='An easy way to provide environ backed config in your projects.',
    long_description=description,
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/confucius',
    py_modules=['confucius'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
