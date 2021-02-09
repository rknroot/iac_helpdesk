# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in iac_helpdesk/__init__.py
from iac_helpdesk import __version__ as version

setup(
	name='iac_helpdesk',
	version=version,
	description='IAC Digital Infrastructure Support Portal',
	author='Eco Data & IAC',
	author_email='rk@ecodata.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
