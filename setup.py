#! /usr/bin/env python
from distutils.core import setup

NAME		= 'teapot'
VERSION 	= '1.1.0'
DESCRIPTION	= 'I\'m a little tea pot'



setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    license="Proprietary",
    packages=['daemonizer', 'daemonizer.test'],
    data_files=[
	    ('/usr/sbin', [ 'usr/sbin/teapotd' ]),
    ]
)
