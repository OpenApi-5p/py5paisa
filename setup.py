#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests",
    "pycryptodome>=3.9.8",
    "certifi>=2020.4.5.1",
    "chardet>=3.0.4",
    "pbkdf2>=1.3",
    "urllib3>=1.25.8",
    "idna>=2.9",
    "loguru>=0.5.1",
    "websocket-client>=0.58.0",
    "pandas>=1.2.4",
]

setup_requirements = []

test_requirements = []

setup(
    author="5paisa",
    author_email='coreteam@5paisa.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6'
    ],
    description=" Python SDK for 5paisa APIs natively written in VB.NET",
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='py5paisa',
    name='py5paisa',
    packages=find_packages(include=['py5paisa', 'py5paisa.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/5paisa/py5paisa',
    version='0.3.1',
    zip_safe=False,
)
