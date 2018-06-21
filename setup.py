from setuptools import setup
from os import path

p = path.abspath(path.dirname(__file__))
readme_filepath = path.join(p, 'README.md')
README = "See https://github.com/danhagen/dsb for full documentation."
if path.isfile(readme_filepath):
    with open(readme_filepath) as f:
        README = f.read()

setup(name='dsb',
      version='0.0.1',
      description='Statusbar function for Python',
      long_description=README,
      long_description_content_type="text/markdown",
      url='http://github.com/danhagen/dsb',
      author='Daniel Hagen',
      author_email='dhagen@usc.edu',
      license='MIT',
      packages=['dsb'],
      install_requires=['termcolor','scipy','numpy'],
      zip_safe=False)
