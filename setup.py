#! /usr/bin/env python
from distutils.core import setup

NAME		= 'teapot'
VERSION 	= '1.2.5'
DESCRIPTION	= 'I\'m a little tea pot'



setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    license="Proprietary",
    packages=['daemonizer', 'daemonizer.test'],
    install_requires=['python-daemon'],
    data_files=[
	    ('/usr/sbin', [ 'usr/sbin/daemonizer' ]),
    ]
)
