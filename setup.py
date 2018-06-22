import setuptools
setuptools.setup(
    name="dsb",
    version="0.0.3",
    url="https://github.com/danhagen/dsb",
    author="Daniel A Hagen",
    author_email="dhagen@usc.edu",
    description="A simple statusbar for python for/while loops.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['termcolor'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

"""
setuptools import setup
from os import path

p = path.abspath(path.dirname(__file__))
readme_filepath = path.join(p, 'README.md')
README = "See https://github.com/danhagen/dsb for full documentation."
if path.isfile(readme_filepath):
    with open(readme_filepath) as f:
        README = f.read()

setup(name='dsb',
      version='0.0.2',
      description='Statusbar function for Python',
      long_description=README,
      long_description_content_type="text/markdown",
      url='http://github.com/danhagen/dsb',
      author='Daniel Hagen',
      author_email='dhagen@usc.edu',
      license='MIT',
      install_requires=['termcolor'],
      zip_safe=False)
 
"""
