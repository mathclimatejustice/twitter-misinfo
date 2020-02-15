import sys
from setuptools import setup

assert sys.version_info.major == 3 and sys.version_info.minor >= 7, \
    "The misinfo repo is designed to work with Python 3.7 and greater." \
    + "Please install it before proceeding."

setup(name="misinfo",
      version="0.0.1",
      install_requires=[],
      description="Twitter Climate change misinformation analysis.",
      author="Math for Climate Justice!",
      )
