# coding: utf-8

from setuptools import setup

with open('requirements_setup.txt') as f:
    required = f.read().splitlines()

setup(
    name='sdbox.core',
    version='0.0.1',
    description='sdbox core',
    author='justworld',
    packages=['sdbox/*'],
    install_requires=required
)
