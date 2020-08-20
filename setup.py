#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Liting Chen",
    author_email='litingchen16@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This is a python implementation of a time management tool (a concentration timer)."
                "Contributions are welcome",
    entry_points={
        'console_scripts': [
            'ctimer=ctimer.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['timer', 'concentration', 'concentrate'],
    name='ctimer',
    packages=find_packages(include=['ctimer', 'ctimer.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/zztin/ctimer',
    version='1.0.0',
    zip_safe=False,
)
