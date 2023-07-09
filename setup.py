#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='querympics',
    description="Une API pour trouver des infos sur les jeux olympiques",
    package_dir={"": "querympics"},
    version="0.3.0",
    packages=find_packages(where="querympics"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    link="https://github.com/gitadum/querympics",
    author="adum",
    author_email="dev@adum.io",
    license="GPL-3.0",
    python_requires="==3.8.*")
