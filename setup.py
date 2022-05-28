# coding=utf-8
import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('poium/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='poium',
    version=version,
    url='https://github.com/SeldomQA/poium',
    license='BSD',
    author='fnngj',
    author_email='fnngj@126.com',
    description='Selenium/appium-based Page Objects test library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Appium-Python-Client>=2.1.0',
        'loguru>=0.6.0',
        'func-timeout>=4.3.5'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    extras_require={
    },
)
