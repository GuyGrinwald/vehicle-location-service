# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Sample package for quickly scaffoling new Python projects',
    long_description=readme,
    author='Guy Grinwald',
    url='https://github.com/GuyGrinwald/sample_python_project',
    license=license,
    packages=find_packages(exclude=('tests'))
)

