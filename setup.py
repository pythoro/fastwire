# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:02:12 2019

@author: Reuben
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastwire",
    version="0.1.3",
    author="Reuben Rusk",
    author_email="pythoro@mindquip.com",
    description="Easy data transfer between classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythoro/fastwire.git",
    download_url="https://github.com/pythoro/fastwire/archive/v0.1.3.zip",
    packages=['fastwire'],
    keywords=['WIRE', 'CONNECTION', 'UTILITY'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[],
)