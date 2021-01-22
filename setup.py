from setuptools import setup

setup(name='emailnetwork',
      version='0.1',
      description='Network graphing utilities for email/mailbox (.mbox) data',
      url='http://github.com/onlyphantom/emailnetwork',
      author='Samuel Chan',
      author_email='s@supertype.ai',
      license='MIT',
      packages=['emailnetwork'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False,
      python_requires='>=3.7')