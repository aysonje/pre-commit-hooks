from setuptools import find_packages
from distutils.core import setup

setup(
    name='Gherkin steps lister',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'list_steps = list_steps.list_steps:main'
        ]
    }
)
