#!/usr/bin/env python

"""The setup script."""

from pathlib import Path
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

HERE = Path(__file__).absolute().parent

requirements = (HERE/".."/"requirements.txt").read_text().split("\n")

setup_requirements = ['pytest-runner', ]

setup(
    author="noce2",
    author_email='20339399+noce2@users.noreply.github.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Examples using GAYA.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gaya',
    name='examples',
    packages=find_packages(include=['examples', 'examples.*']),
    setup_requires=setup_requirements,
    url='https://github.com/open-mech-eng/gaya/tree/master/examples',
    version='0.1.0',
    zip_safe=False,
)
