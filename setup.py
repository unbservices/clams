"""
Clams
=====

Create simple, nested, command-line interfaces.

"""

import os
from setuptools import setup, find_packages


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE_PATH = os.path.join(PROJECT_DIR, 'VERSION')


def read_version():
  if not os.path.isfile(VERSION_FILE_PATH):
    raise EnvironmentError("Version file not found.")
  with open(VERSION_FILE_PATH) as f:
    return f.read().strip()


if __name__ == '__main__':
  setup(
    name='clams',
    version=read_version(),
    description='Create simple, nested, command-line interfaces.',
    author='Nick Zarczynski',
    author_email='nick@unb.services',
    url='https://github.com/unbservices/clams',
    license='MIT',
    packages=['clams'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: OS Independent',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 2 :: Only',
      'Programming Language :: Unix Shell',
      'Topic :: Software Development :: Libraries',
      'Topic :: Software Development :: Libraries :: Application Frameworks',
      'Topic :: Software Development :: User Interfaces',
      'Topic :: Utilities',
    ],
  )
