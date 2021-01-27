from setuptools import setup, find_packages
from pathlib import Path
from emailnetwork.version import __version__

setup(name='emailnetwork',
      version=__version__,
      description='Network graphing utilities for email/mailbox (.mbox) data',
      long_description=(Path(__file__).parent/'README.md').read_text(),
      long_description_content_type='text/markdown',
      url='http://github.com/onlyphantom/emailnetwork',
      author='Samuel Chan',
      author_email='s@supertype.ai',
      license='MIT',
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=['matplotlib', 'networkx'],
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
      ],
      zip_safe=False,
      python_requires='>=3.7')