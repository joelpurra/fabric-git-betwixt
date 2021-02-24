from distutils.core import setup

setup(
    name='betwixt',
    version='1.0',
    description='Selective fabric deployment of compiled projects using git repositories',
    author='Joel Purra',
    author_email='code+betwixt@joelpurra.com',
    url='https://joelpurra.com/',
    packages=['betwixt'],
    requires=['fabric', 'gitric'])
