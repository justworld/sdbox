# coding: utf-8

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='djangosimpletest',
    version='0.0.1',
    description='django test simple framework',
    author='justworld',
    packages=['simple_test'],
    install_requires=required,
)
