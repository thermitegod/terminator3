#!/usr/bin/env python3
#    Terminator.optionparse - Parse commandline options
#    Copyright (C) 2006-2010  cmsj@tenshu.net
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 2 only.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
"""Terminator.optionparse - Parse commandline options"""

import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, REMAINDER

from terminatorlib import config, util, version
from terminatorlib.translation import _
from terminatorlib.util import dbg, err


class C:
    pass


options = C()


def parse_options():
    """Parse the arguments"""

    argslist = [
        (('-v', '--version',),
         dict(action='version', version='%(prog)s {}'.format(version.APP_VERSION),
              help=_('Display program version'))),
        (('-m', '--maximise',),
         dict(action='store_true', dest='maximise',
              help=_('Maximize the window'))),
        (('-f', '--fullscreen',),
         dict(action='store_true', dest='fullscreen',
              help=_('Make the window fill the screen'))),
        (('-b', '--borderless',),
         dict(action='store_true', dest='borderless',
              help=_('Disable window borders'))),
        (('-H', '--hidden',),
         dict(action='store_true', dest='hidden',
              help=_('Hide the window at startup'))),
        (('-T', '--title',),
         dict(action='store', dest='forcedtitle', metavar='TITLE',
              help=_('Specify a title for the window'))),
        (('--geometry',),
         dict(action='store', dest='geometry', type=str, metavar='GEOMETRY',
              help=_('Set the preferred size and position of the window (see X man page)'))),
        (('-g', '--config',),
         dict(action='store', dest='config', metavar='CONFIG',
              help=_('Specify a config file'))),
        (('--working-directory',),
         dict(action='store', dest='working_directory', metavar='DIR',
              help=_('Set the working directory'))),
        (('-i', '--icon',),
         dict(action='store', dest='forcedicon', metavar='ICON',
              help=_('Set a custom icon for the window (by file or name)'))),
        (('-r', '--role',),
         dict(action='store', dest='role', metavar='ROLE',
              help=_('Set a custom WM_WINDOW_ROLE property on the window'))),
        (('-l', '--layout',),
         dict(action='store', dest='layout', default='default',
              help=_('Launch with the given layout'))),
        (('-s', '--select-layout',),
         dict(action='store_true', dest='select',
              help=_('Select a layout from a list'))),
        (('-p', '--profile',),
         dict(action='store', dest='profile', default='default',
              help=_('Use a different profile as the default'))),
        (('-u', '--no-dbus',),
         dict(action='store_true', dest='nodbus',
              help=_('Disable DBus'))),
        (('-d', '--debug',),
         dict(action='count', dest='debug', default=0,
              help=_('Enable debugging information (twice for debug server)'))),
        (('--debug-classes',),
         dict(action='store', dest='debug_classes',
              help=_('Comma separated list of classes to limit debugging to'))),
        (('--debug-methods',),
         dict(action='store', dest='debug_methods',
              help=_('Comma separated list of methods to limit debugging to'))),
        (('--new-tab',),
         dict(action='store_true', dest='new_tab',
              help=_('If Terminator is already running, just open a new tab'))),
        (('-e', '--execute',),
         dict(action='store', dest='execute', nargs=REMAINDER,
              help=_('Use the rest of arguments as a command to execute'))),
    ]

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    for args, kwargs in argslist:
        parser.add_argument(*args, **kwargs)

    parser.parse_args(namespace=options)

    if options.debug_classes or options.debug_methods:
        if not options.debug > 0:
            options.debug = 1

    if options.debug:
        util.DEBUG = True
        if options.debug > 1:
            util.DEBUGFILES = True
        if options.debug_classes:
            classes = options.debug_classes.split(',')
            for item in classes:
                util.DEBUGCLASSES.append(item.strip())
        if options.debug_methods:
            methods = options.debug_methods.split(',')
            for item in methods:
                util.DEBUGMETHODS.append(item.strip())

    if options.working_directory:
        path = os.path.expanduser(options.working_directory)
        if os.path.isdir(path):
            options.working_directory = path
            os.chdir(path)
        else:
            err('OptionParse::parse_options: %s does not exist' % path)
            options.working_directory = None

    configobj = config.Config()

    if options.layout not in configobj.list_layouts():
        options.layout = 'default'
    if options.profile not in configobj.list_profiles():
        options.profile = 'default'

    if util.DEBUG == True:
        dbg('OptionParse::parse_options: command line options: %s' % options)
